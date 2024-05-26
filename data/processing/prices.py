import numpy as np
import pandas as pd

from config import ANNUAL_TRADING_DAYS


def calculate_daily_return(adjusted_close_prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates total daily return from adjusted prices, close to close
    """
    return adjusted_close_prices.pct_change(fill_method=None)


def calculate_implied_market_return(
    adjusted_close_price_return: pd.DataFrame,
) -> pd.DataFrame:
    """
    Infer the market return from the equal-weighted return of all stocks
    """
    return adjusted_close_price_return.mean(axis=1)


def calculate_trailing_volatility(
    adjusted_close_price_return: pd.DataFrame,
    lookback=60,
    exponential=True,
    lower_clip=0.05,
) -> pd.DataFrame:
    if exponential:
        trailing_volatility = adjusted_close_price_return.ewm(
            lookback, min_periods=int(lookback * 0.75)
        ).std() * np.sqrt(ANNUAL_TRADING_DAYS)
    else:
        trailing_volatility = adjusted_close_price_return.rolling(
            lookback, min_periods=int(lookback * 0.75)
        ).std() * np.sqrt(ANNUAL_TRADING_DAYS)
    return trailing_volatility.clip(lower=0.02)
