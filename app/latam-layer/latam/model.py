import pandas as pd
import xgboost as xgb

#Hyperparameters
DEFAULT_CLASSIFICATION_PARAMS = {
    'objective': 'binary:logistic',
    'max_depth': 10,
    'learning_rate': 0.001,
}

PATH_TO_MODEL = '../data/model.bin'

class Model:
    """    This class will be one responsible for modeling our data. XGboost Algorithm will be used
    as it supports both categorical and numerical variables, it handles a lot of tasks internally,
    such as cross validation, bagging, boosting, and provides feature importance metrics.
    """
    def __init__(self) -> None:
        self.X = None
        self.Y = None
        self.dmatrix = None
        # XGBoost library will auto-detect if the problem is classification or regression based on the target values
        self.model = xgb.XGBRegressor()        

    def load_dataset(self,X: pd.DataFrame, Y: pd.Series) -> None:
        self.X = X
        self.Y = Y
        self.dmatrix = xgb.DMatrix(X, label=Y)

    def fit(self):
        self.model.fit(self.X, self.Y)
        self.model_trained = True

    def feature_importance(self):
        """
        XGBoost provides a way to examine the importance of each feature in the original dataset within the model.
        It is recommended to do this with the complete set of datapoints.
        """
        if not self.model_trained:
            raise Exception('Model is not trained')
        
        feature_names = self.X.columns
        feature_importance = dict(zip(feature_names, self.model.feature_importances_))
        sorted_feature_importance = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        return sorted_feature_importance

    def cv(self):
        return xgb.cv(DEFAULT_CLASSIFICATION_PARAMS, self.dmatrix, num_boost_round=10, nfold=5, metrics='logloss', seed=42)
    
    @staticmethod
    def predict(model: xgb.XGBRegressor, X: pd.DataFrame) -> pd.DataFrame:
        return model.predict(X)
    
    def save(self, path: str = None) -> None:
        model_path = path if path is not None else PATH_TO_MODEL
        self.model.save_model(model_path)

    def load(self, path: str = None) -> None:
        model_path = path if path is not None else PATH_TO_MODEL
        self.model.load_model(model_path)
        self.model_trained = True
        print(f"Model loaded from {model_path}")


