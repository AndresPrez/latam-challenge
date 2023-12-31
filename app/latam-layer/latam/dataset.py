import numpy as np
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split
from collections import Counter
import pandas as pd
from datetime import datetime
from latam.synthetic_features import SyntheticFeatures
from latam.statistics import robust_zscore, zscore

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

INPUT_COLUMNS = [
    "Fecha-I",
    "Vlo-I",
    "Ori-I",
    "Des-I",
    "Emp-I",
    "DIA",
    "MES",
    "AÑO",
    "TIPOVUELO",
    "OPERA",
    "SIGLAORI",
    "SIGLADES",
    "Temporada alta",
    "Periodo día",
]

OUTPUT_COLUMNS = [
    'Atraso menor', # This is the target for classification
    'Diferencia en minutos' # This is the target for regression
]

COLUMNS_PARSER = {
    "Fecha-I": pd.to_datetime
}

COLUMNS_DTYPE = {
    "Fecha-I": 'datetime64[ns]',
    "Vlo-I": 'category',
    "Ori-I": 'category',
    "Des-I": 'category',
    "Emp-I": 'category',
    "DIA": int,
    "MES": int,
    "AÑO": int,
    "TIPOVUELO": 'category',
    "OPERA": 'category',
    "SIGLAORI": 'category',
    "SIGLADES": 'category',
    "Temporada alta": bool,
    "Periodo día": 'category',
    'Diferencia en minutos': int
}

SUPPORTED_ANOMALY_SORES = [
    'r-zscore',
    'zscore'
]

CATEGORICAL_ENCODER_FILE = '../data/categorical_encoder.pickle'

TWO_PI = 2*np.pi

def target_encoding(cat_values: pd.Series, target_values: pd.Series) -> pd.Series:
    """
    This method will compute the target encoding for a given categorical feature.
    Target encoding is particularly useful when dealing with high cardinality features.
    When cardinality is low, it behaves similar to counter encoding.

    Target Encoding may lead to overfitting but XGBoost has some nice overfitting handling, so we should be fine.
    """
    df = pd.DataFrame({'cat': cat_values, 'target': target_values})
    target_encoding = {}
    cat_count_map = Counter(cat_values)
    for cat_value in cat_count_map.keys():
        mean_target = np.round(df[df['cat'] == cat_value]['target'].mean(), 3)
        target_encoding[cat_value] = mean_target
    
    return target_encoding
    # return cat_values.apply(lambda X: target_encoding[X])

def split_date(date_values: datetime) -> pd.DataFrame:
    """
        This method will split a date column into its components (year, month, day, hour).
    """
    date_columns = {
        'year': [date_values.year],
        'month': [date_values.month],
        'day': [date_values.day],
        'hour': [date_values.hour]
    }
    return pd.DataFrame(date_columns)

def date_encoding(date_values: pd.Series) -> pd.DataFrame:
    """
        For date values, cyclic encoding will be used so that the model can
        levarage the cyclic nature of months, days, and hours.
    """
    rows = date_values.apply(split_date)
    date_df = pd.concat(list(rows))
    date_cyclic_encoding = {}
    date_cyclic_encoding['year'] = date_df['year'] # Year is not encoded in a cyclic manner, just keep it as number
    date_cyclic_encoding['month'] = date_df['month'].apply(lambda X: np.cos( TWO_PI * X / 12)).apply(lambda x: np.round(x, 3))
    date_cyclic_encoding['day'] = date_df['day'].apply(lambda X: np.cos( TWO_PI * X / 31)).apply(lambda x: np.round(x, 3))
    date_cyclic_encoding['hour'] = date_df['hour'].apply(lambda X: np.cos( TWO_PI * X / 24)).apply(lambda x: np.round(x, 3))

    return pd.DataFrame(date_cyclic_encoding)


class Dataset:
    """
    This class will be responsible for data pre-processing (i.e., preparation, cleaning and formatting).
    """

    def __init__(
            self,
            dataset_file: pd.DataFrame = None,
            dataset: pd.DataFrame = None
        ) -> None:
        self.dataset = dataset
        self.encoded_dataset = None
        self.anomalies_removed = False

        if dataset_file:
            self.dataset = pd.read_csv(dataset_file)
        elif dataset is not None:
            self.dataset = dataset
        else:
            raise Exception("Either dataset_file or dataset dataframe must be provided.")
        
    @staticmethod
    def compute_synthetic_features(X:pd.DataFrame) -> None:
        sf = SyntheticFeatures(X)
        sf_df = sf.compute()
        return pd.concat([sf_df, X], axis=1)

    def clean(self) -> None:
        X = Dataset.compute_synthetic_features(self.dataset)
        X = Dataset.get_relevant_columns(X)
        X = Dataset.handle_missing_values(X)
        X = Dataset.parse(X)
        self.dataset = X
        self.is_data_clean = True

    def encode(self, encoding_file: str) -> None:
        """
        This method will be responsible for encoding the columns into a better representation.
        """
        if not self.is_data_clean:
            raise Exception("Data must be cleaned before encoding.")
        
        categoric_cols = self.get_categoric_features()
        date_cols = self.get_date_features()
        newDataset = self.dataset.copy()
        # We'll need to store the encoding map so that we can use it later for the API.
        using_saved_encoding = self.load_cat_encodings(encoding_file)
        for cat_col in categoric_cols:
            # This encoding replaces the categorical value with the mean of the target for that value
            cat_col_values = categoric_cols[cat_col]

            # If the encoding map is not available, compute it.
            if using_saved_encoding:
                target_encoder = self.cat_encoding_map[cat_col]
            else:
                target_encoder = target_encoding(cat_col_values, self.dataset[OUTPUT_COLUMNS[1]])

            self.cat_encoding_map[cat_col] = target_encoder
            newDataset[cat_col] = [target_encoder[cat_value] for cat_value in cat_col_values]
        
        for date_col in date_cols:
            # This encoding splits the date into its components (year, month, day, hour), so more columns are created.
            cyclic_date_columns = date_encoding(date_cols[date_col]).reset_index(drop=True)
            newDataset = pd.concat([cyclic_date_columns, newDataset], axis=1)
            newDataset = newDataset.drop(columns=[date_col])
            
        self.encoded_dataset = newDataset

        if not using_saved_encoding:
            self.save_cat_encodings(encoding_file)

    def save_cat_encodings(self, encoding_file: str = None) -> None:
        encoding_path = encoding_file if encoding_file is not None else CATEGORICAL_ENCODER_FILE
        with open(encoding_path, 'wb') as file:
            pickle.dump(self.cat_encoding_map, file)

    def load_cat_encodings(self, encoding_file:str = None) -> bool:
        """
        Loads an existing categorical encoding map, if available.
        """
        encoding_path = encoding_file if encoding_file is not None else CATEGORICAL_ENCODER_FILE
        if Path(encoding_path).exists():
            with open(encoding_path, 'rb') as file:
                self.cat_encoding_map = pickle.load(file)
            print(f"Categorical encodings loaded from {encoding_path}")
            return True
        else:
            self.cat_encoding_map = {}
            return False
            
    def split_target(self, for_regression = True) -> (pd.DataFrame, pd.Series):
        """
        This method will be responsible for splitting the target column from the dataset.
        """
        
        if self.encoded_dataset is None:
            raise Exception("Data must be encoded first.")
        
        df_to_use = self.encoded_dataset.copy()
        
        target_column = OUTPUT_COLUMNS[1] if for_regression else OUTPUT_COLUMNS[0]

        X, Y = None, None
        if target_column in df_to_use.columns:
            Y = df_to_use[target_column]

        X = df_to_use
        try:
            X.drop(columns=OUTPUT_COLUMNS, inplace=True)
        except:
            pass
        
        return X, Y

    def split_test_train(self, for_regression = True):
        X, Y = self.split_target(for_regression)
        return train_test_split(X, Y, test_size=0.2, random_state=42)

    def get_categoric_features(self) -> pd.DataFrame:
        if not self.is_data_clean:
            raise Exception("Data must be cleaned first.")
        return self.dataset.select_dtypes(include=['category'])
    
    def get_date_features(self) -> pd.DataFrame:
        if not self.is_data_clean:
            raise Exception("Data must be cleaned first.")
        return self.dataset.select_dtypes(include=['datetime64[ns]'])

    @staticmethod
    def compute_anomaly_scores(X:pd.DataFrame) -> None:
        """
        This method will be responsible for removing anomalies from the dataset.
        A datapoint will be considered an anomaly if the chose criterion is above the treshold.
        """
        new_df = X.copy()
        new_df['r-zscore'] = robust_zscore(new_df[OUTPUT_COLUMNS[1]])
        new_df['zscore'] = zscore(new_df[OUTPUT_COLUMNS[1]])

        return new_df
    
    def remove_anomalies(self, threshold = None, criterion = 'r-zscore') -> None:
        """
        This method will be responsible for removing anomalies from the dataset.
        A datapoint will be considered an anomaly if the chose criterion is above the treshold.
        """
        X = self.dataset.copy()
        new_df = Dataset.compute_anomaly_scores(X)
        
        if criterion not in SUPPORTED_ANOMALY_SORES:
            raise Exception(f"Criterion {criterion} not supported. Must be either 'r-zscore' or 'zscore'")

        new_df = new_df[new_df[criterion] < threshold]
        new_df = new_df.drop(columns=SUPPORTED_ANOMALY_SORES)
        new_df = new_df.reset_index(drop=True)

        percetange_removed = np.round(((X.shape[0] - new_df.shape[0]) / X.shape[0]) * 100, 3)
        print(f"Reduced dataset by {percetange_removed}% after removing outliers")

        self.dataset = new_df
        
    @staticmethod
    def get_relevant_columns(X: pd.DataFrame) -> pd.DataFrame:
        """
            Only keep use the useful columns
        """
        new_X = {}
        relevant_columns = INPUT_COLUMNS+OUTPUT_COLUMNS
        for column in relevant_columns:
            if column in X:
                new_X[column] = X[column].values
                
        return pd.DataFrame(new_X)

    @staticmethod
    def get_input_columns(X: pd.DataFrame) -> pd.DataFrame:
        """
            Only keep use the useful columns
        """
        new_X = {}
        for column in INPUT_COLUMNS:
            if column in X:
                new_X[column] = X[column].values

        return pd.DataFrame(new_X)
    
    @staticmethod
    def handle_missing_values(X: pd.DataFrame) -> pd.DataFrame:
        """
            This handles any row with missing data. By default it will drop the row. 
            More sofisticated methods can be later implemented.
        """
        return X.dropna().reset_index(drop=True)
    
    @staticmethod
    def parse(
        X: pd.DataFrame,
    # This method could be made generic by using something like a columns_config argument
    # that would be the COLUMNS_PARSER and COLUMNS_DTYPE dicts needed for the preprocessing.
        # columns_config: Dict[str, Dict[str, any]]
    ) -> pd.DataFrame:
        newX = X.copy()
        for key, value in COLUMNS_PARSER.items():
            if key in X:
                newX[key] = X[key].apply(value)

        for key, value in COLUMNS_DTYPE.items(): 
            if key in X:
                newX[key] = X[key].astype(value)

        return newX
