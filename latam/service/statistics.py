import pandas as pd
from scipy.stats import median_abs_deviation

def robust_zscore(X: pd.Series):
    """
        This method will calculate the robust zscore for a given column.
    """
    median = X.median()
    mad = median_abs_deviation(X)
    return 0.6745 * (X - median) / mad

def zscore(X: pd.Series):
    """
        This method will calculate the zscore for a given column.
    """
    mean = X.mean()
    std = X.std()
    return (X - mean) / std
