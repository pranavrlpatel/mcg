import pandas as pd
from statsmodels.tsa.stattools import adfuller

def load_and_prepare_series(filepath: str, date_col: str, value_col: str) -> pd.Series:
    df = pd.read_csv(filepath, parse_dates=[date_col])
    
    # Check if the frequency can be parsed, else we might have duplicate dates or NaT issues.
    df = df.set_index(date_col)
    
    # yfinance column for date might be 'Date' and value 'Close'.
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
        
    # The data mock might have strings for dates or different formats.
    df = df.resample('ME').mean()
    series = df[value_col].dropna()

    # Z-score normalisation (removes scale differences, not stationarity)
    if series.std() != 0:
        series = (series - series.mean()) / series.std()

    # ADF stationarity test — REQUIRED before Granger
    adf_result = adfuller(series, autolag='AIC')
    p_value = adf_result[1]

    if p_value > 0.05:
        print(f"[loader] {value_col} is NON-STATIONARY (ADF p={p_value:.3f}) — applying first differencing")
        series = series.diff().dropna()
        # Re-test
        adf_result2 = adfuller(series, autolag='AIC')
        print(f"[loader] After differencing: ADF p={adf_result2[1]:.3f}")
    else:
        print(f"[loader] {value_col} is stationary (ADF p={p_value:.3f}) ✓")

    return series
