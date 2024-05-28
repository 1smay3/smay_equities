"""Click-ified script to gather and data_cache data from data API"""

import logging
import click
from fmp import fmp_data
from data.data_cache.definitions import LOCAL_ARCTIC_PATH
from data.data_cache.arctic import ArcticHandler

COUNT_DEBUG_NUMBER_OF_SYMBOLS = 10

logger = logging.getLogger(__name__)

arctic_store = ArcticHandler(LOCAL_ARCTIC_PATH)

def get_all_stock_symbols(symbol):
    all_symbols = fmp_data.gather_symbols_from_index_no_survivorship(symbol)
    return all_symbols


def get_many_stock_prices(symbols):
    all_prices = fmp_data.gather_simple_prices(symbols)
    return all_prices



@click.command()
def get_stock_and_index_data():
    spx_constituents = get_all_stock_symbols("sp500_constituent")
    all_stock_prices = get_many_stock_prices(spx_constituents[:COUNT_DEBUG_NUMBER_OF_SYMBOLS])

    # Save prices to arctic
    arctic_store.save_dataframe_to_arctic(arctic_library_name="equities", data=all_stock_prices, symbol="equities")


if __name__ == "__main__":
    get_stock_and_index_data()
