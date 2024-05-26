"""SingleStockData class which takes in the raw response from the API
which is often prices of fundamental data, and then applies pre-processing
and passes the processed

"""

import os

import polars as pl

from config import PRICE_FIELD_NAME
from data.processing.generic import sanity_clean_data
from data.processing.prices import (
    calculate_daily_return,
    calculate_implied_market_return,
    calculate_trailing_volatility,
)
from definitions import ROOT_DIR
from factor_model.beta.beta import compute_rolling_beta


class SingleStockDataStore:
    """
    Core datastore class which loads single-stock data (currently only locally), applys processing,
    and passes into attributes for access elsewhere
    """

    def __init__(
        self, symbol="spx", data_root_folder="data", data_sub_folder="data_cache"
    ):
        self.symbol = symbol

        # Construct the relative path to the raw data file
        single_stock_data_file = f"{self.symbol}_ss.pkl"

        self.raw_single_stock_data_path = os.path.join(
            ROOT_DIR, data_root_folder, data_sub_folder, single_stock_data_file
        )

        # Load raw data from file
        self.raw_single_stock_data = pl.read_pickle(self.raw_single_stock_data_path)

        # Process data and generate attributes
        self.adjusted_close = sanity_clean_data(
            self.raw_single_stock_data[PRICE_FIELD_NAME]
        )
        self.daily_return = calculate_daily_return(self.adjusted_close)
        self.market_return = calculate_implied_market_return(self.daily_return)
        self.stock_volatility = calculate_trailing_volatility(self.daily_return)


class IndexLevelDataStore:
    """
    Core datastore class which loads index-level data (currently only locally), apply's processing,
    and passes into attributes for access elsewhere
    Note: All indexes are currently stored in the same file, so there is no concept of symbol here.
    Passing an argument into the IndexLevelDataStore as you would with the StockLevelDataStore will
    lead to issues as it will overwrite the first arg, data_root_folder
    """

    def __init__(self, data_root_folder="data", data_sub_folder="data_cache"):
        # Construct the relative path to the raw data file
        index_level_data_file = "indexes.pkl"

        self.raw_index_level_data_path = os.path.join(
            ROOT_DIR, data_root_folder, data_sub_folder, index_level_data_file
        )

        # Load raw data from file
        self.raw_index_level_data = pl.read_pickle(self.raw_index_level_data_path)

        # Process data and generate attributes
        self.adjusted_close = sanity_clean_data(
            self.raw_index_level_data[PRICE_FIELD_NAME]
        )

        self.daily_return = calculate_daily_return(self.adjusted_close)


class DataStore:
    """
    Class to manage both SingleStockDataStore and IndexLevelDataStore instances, and
    for any attributes which distinctly refer/require both stock and index data.
    """

    def __init__(
        self,
        single_stock_symbol: str = "spx",
        data_root_folder: str = "data",
        data_sub_folder: str = "data_cache",
    ):
        # Create SingleStockDataStore instance
        self.SingleStock = SingleStockDataStore(
            symbol=single_stock_symbol,
            data_root_folder=data_root_folder,
            data_sub_folder=data_sub_folder,
        )

        # Create IndexLevelDataStore instance
        self.IndexLevel = IndexLevelDataStore(
            data_root_folder=data_root_folder, data_sub_folder=data_sub_folder
        )

        self.beta_5y = compute_rolling_beta(self, returns_resample="M", lookback=60)
        self.beta_3y = compute_rolling_beta(self, returns_resample="M", lookback=36)
        self.beta_1y = compute_rolling_beta(self, returns_resample="M", lookback=12)
