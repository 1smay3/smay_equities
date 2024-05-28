"""
Calls to the FMP API service and then creates DataFrames / higher level types from the retrieved information
"""

import logging
from typing import List

import polars as pl
from fmpsdk.url_methods import __return_json_v3

import repository.fmp_api_service as api_service
from data.processing.polars import concatenate_dataframes
from fmp.models.stock import Stock

# Create a logger
logger = logging.getLogger(__name__)


def _parse_and_filter_symbol_list(
    symbol_list: List[Stock], filter_dictionary: dict
) -> pl.DataFrame:
    """
    Get the symbnol list from the data API, and filter_dictionary to only
    the conditions passed by the user, e.g:
    ["type":"stock", "exchange": "NASDAQ"}
    :param symbol_list
        Unadjusted list from the API
    :param filter_dictionary
        Dictionary of conditions to filter_dictionary on in the form
        "column_name":"condition", as we pass symbol_list to a pl.DataFrame
    :return: [pl.DataFrame]
        [pl.DataFrame] version of JSON from API, filtered given the conditions provided
    """

    dataframe = pl.DataFrame(symbol_list)

    if (
        not filter_dictionary
    ):  # If no filters are provided, return the original DataFrame
        return dataframe

    # Apply filters based on provided column names and values
    for column, value in filter_dictionary.items():
        if column in dataframe.columns:
            dataframe = dataframe[dataframe[column] == value]
        else:
            print(
                f"Warning: Column '{column}' not found in the DataFrame."
                f" Skipping filter_dictionary for this column."
            )
    return dataframe


def _get_constituents(apikey, symbol):
    """
    NOTE: This includes survivorship bias. In the future,
    add logic that takes the /historical/xyz endpoint
    and generates a non-biased list/timeseries
    :param apikey: Your API key.
    :param symbol: Company ticker.
    :return: A list of dictionaries.


    Query FMP /historical-price-full/<ticker> API

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :return: A list of dictionaries.
    """
    query_vars = {"apikey": apikey}
    return __return_json_v3(path=symbol, query_vars=query_vars)


def _get_constituents_no_survivorship(apikey, symbol):
    """
    Get all historic constituents for an index
    :param apikey: Your API key.
    :param symbol: Company ticker.
    :return: A list of dictionaries.


    Query FMP /historical-price-full/<ticker> API

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :return: A list of dictionaries.
    """
    path = f"/historical/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_v3(path=path, query_vars=query_vars)


def gather_detailed_prices(api_key, symbol):
    """
    Function to be exposed externally to gather a price dataframe 'raw'
    from the API and pass to a pandas DataFrame
    """
    historical_prices_resp = api_service.get_historic_prices(api_key)
    detailed_prices = pl.DataFrame(historical_prices_resp).set_index("date")
    return detailed_prices


def gather_symbols_from_index(symbol):
    """
    Get index constituents from API, before passing to a dataframe and filtering.
    This includes survivorship bias, as it only includes stocks which are in the index
    'now'. The row-wise count of the data since 1990 will be increasing throughout time,
    and empirically only around 200 of the names that are still in the index were
    in the index in the 70s or so, showing the benefit in the complete list
    """
    raw_constituents = api_service.get_constituents(symbol)
    constituents_dataframe = pl.DataFrame(raw_constituents)

    # TODO: Consolidate "sorted"
    mapped = constituents_dataframe.map(lambda constituent: constituent.symbol)
    return sorted(list(set(mapped.values.flatten())))


def gather_symbols_from_index_no_survivorship(symbol):
    """
    Get index constituents from API, before passing to a dataframe and filtering.
    This removes survivorship bias by considering all names which have ever been
    in the index
    """
    raw_constituents = api_service.get_constituents_no_survivorship_bias(symbol)
    constituents_list = [x.symbol for x in raw_constituents]
    no_duplicates_list = sorted(list(set(constituents_list)))
    return no_duplicates_list


PRICES_DATETIME_FORMAT = "%Y-%m-%d"


def gather_simple_prices(symbols_strings, field="adjClose") -> pl.DataFrame:
    """
    Function to be exposed externally to gather prices for many tickers for a single
    field. This is intended to use as to get our (dates x stocks) format
    """
    all_symbols_data = []
    prices = api_service.get_historic_prices(symbols_strings)
    for price_info in prices:
        if price_info:
            simple_prices_df = pl.DataFrame(price_info["historical"])[["date", field]]
            simple_prices_df = simple_prices_df.with_columns(
                pl.col("date").str.strptime(
                    pl.Date, format=PRICES_DATETIME_FORMAT, strict=False
                )
            )
            simple_prices_df = simple_prices_df.rename(
                {"adjClose": price_info["symbol"]}
            )
            all_symbols_data.append(simple_prices_df)

    return concatenate_dataframes(all_symbols_data).sort("date")
