import pandas as pd

def preprocess(
    df: pd.DataFrame
) -> pd.DataFrame:
    
    if df.empty:
        raise ValueError('Empty dataframe')
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError('Index not datetime')
    
    data = df.copy()
    data = data.loc[data.index.notna()]
    data = data.sort_index()

    if data.empty:
        raise ValueError('No valid observation')
    
    return data