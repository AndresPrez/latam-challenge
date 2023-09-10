from typing import List, Tuple, Dict
from datetime import datetime
import pandas as pd

HIGH_SEASONS: List[Tuple[Tuple[int, int]]] = [
    ((12, 15), (3, 3)),
    ((7, 15), (7, 31)),
    ((9, 11), (9, 30)),
]

DAY_PERIODS: Dict[str, Tuple[Tuple[int, int]]] = {
    "mañana": ((5, 0), (11, 59)),
    "tarde": ((12, 0), (18, 59)),
    "noche": ((19, 0), (4, 59)),
}

class SyntheticFeatures:

    def __init__(self, df:pd.DataFrame):
        self.df = df
  
    def compute(self) -> pd.DataFrame:
        syntheticFeatures = pd.DataFrame()

        syntheticFeatures['Temporada alta'] = SyntheticFeatures.isHighSeason(self.df['Fecha-I'])
        syntheticFeatures['Diferencia en minutos'] = SyntheticFeatures.minutesDelay(self.df['Fecha-I'], self.df['Fecha-O'])
        syntheticFeatures['Atraso menor'] = SyntheticFeatures.isMinorDelay(syntheticFeatures['Diferencia en minutos'])
        syntheticFeatures['Periodo día'] = SyntheticFeatures.flightDayPeriod(self.df['Fecha-I'])

        return syntheticFeatures
    
    @staticmethod
    def isHighSeason(dates: pd.Series) -> pd.Series:
        def check(date: datetime) -> bool:
            """Checks if the date is between the periods of high season."""
            for highSeason in HIGH_SEASONS:
                start = datetime(date.year, highSeason[0][0], highSeason[0][1])
                end = datetime(date.year, highSeason[1][0], highSeason[1][1])

                # check if the date is between the season months.
                if start <= date <= end:
                    return True
                
                # If the start month is grater than the end month, then it's a cross year period.
                is_cross_year_period = highSeason[0][0] > highSeason[1][0]
                if is_cross_year_period and (date >= start or date <= end):
                    return True

            return False
        
        return dates.apply(pd.to_datetime).apply(check)
    
    @staticmethod
    def minutesDelay(x: pd.Series, y: pd.Series) -> pd.Series:
        return (pd.to_datetime(y) - pd.to_datetime(x)).dt.total_seconds() / 60
    
    @staticmethod
    def isMinorDelay(minuteDelays: pd.Series) -> pd.Series:
        return minuteDelays.apply(lambda x: x <= 15)
    
    @staticmethod
    def flightDayPeriod(dates: pd.Series) -> pd.Series:
        def getDayPeriod(date: datetime):
            """Returns the day period of the date."""
            for dayPeriodLabel, dayPeriod in DAY_PERIODS.items():
                start = datetime(date.year, date.month, date.day, dayPeriod[0][0], dayPeriod[0][1])
                end = datetime(date.year, date.month, date.day, dayPeriod[1][0], dayPeriod[1][1])

                # check if the date is between the day period.
                if start <= date <= end:
                    return dayPeriodLabel
                
                # If the start hour is grater than the end hour, then it's a cross day period.
                is_cross_day_period = dayPeriod[0][0] > dayPeriod[1][0]
                if is_cross_day_period and (date >= start or date <= end):
                    return dayPeriodLabel
  
        return dates.apply(pd.to_datetime).apply(getDayPeriod)


if __name__ == "__main__":
    # Read the data from the provided csv file.
    csv_data = pd.read_csv("./dataset.csv")
    # Compute the synthetic features.
    sf = SyntheticFeatures(csv_data)
    sf_df = sf.compute()
    # Stores the synthetic features in a csv file.
    sf_df.to_csv("./synthetic_features.csv", index=False)