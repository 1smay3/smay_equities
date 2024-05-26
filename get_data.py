"""Click-ified script to gather and data_cache data from data API"""

import logging

import click

from data.schedule import (data_name_to_endpoint_mapping,
                           index_level_data_mapping,
                           index_level_symbol_mapping,
                           map_field_name_to_function,
                           single_stock_data_mapping)
from fmp import fmp_data
from data.data_cache.arctic import save_dataframe_to_arctic

COUNT_DEBUG_NUMBER_OF_SYMBOLS = 200

logger = logging.getLogger(__name__)


def get_single_stock_data(data_save_path):
    """
    For the parsed type and exchange (from our config), gather the relevant data
    and data_cache in a format accessible for research (dates x stocks)
    :param data_save_path: str
        The path to use when pickling
    :return: None
    """
    # Run for all elements of the schedule
    for index_name, field_name in single_stock_data_mapping.items():
        stock_index_endpoint_name = data_name_to_endpoint_mapping[index_name]

        # TODO this should be a list of strings

        remote_symbols_from_index = fmp_data.gather_symbols_from_index_no_survivorship(
            stock_index_endpoint_name
        )[:COUNT_DEBUG_NUMBER_OF_SYMBOLS]

        # Use the function_map to apply the respective functions
        # TODO: Change this implementation, its pretty unclear how its structured
        result = {}
        for field in field_name:
            if field in map_field_name_to_function:
                function_to_apply = map_field_name_to_function[field]
                # TODO: What if these functions have different args? We shouldn't do this IMO
                result[field] = function_to_apply(remote_symbols_from_index)

        save_dataframe_to_arctic("equities", result["historic_price_full"], "adjusted_prices")
        print("Saved Stock Level Data")


def get_index_level_data(data_save_path):
    # Run for all elements of the schedule
    for field_name, index_list in index_level_data_mapping.items():
        index_symbols = [
            index_ticker
            for readable_index_symbol, index_ticker in index_level_symbol_mapping.items()
            if readable_index_symbol in index_list
        ]

        # Use the function_map to apply the respective functions
        result = {}

        if field_name in map_field_name_to_function:
            function_to_apply = map_field_name_to_function[field_name]
            # TODO: What if these functions have different args? We shouldn't do this IMO
            result[field_name] = function_to_apply(index_symbols)

        save_dataframe_to_arctic("equities", result["historic_price_full"], "adjusted_prices")
        print("Saved Index Level Data")


@click.command()
@click.option(
    "--data_save_path",
    help="Pass path to save data to",
    required=True,
    default="data/data_cache",
)
def get_stock_and_index_data(data_save_path):
    get_single_stock_data(data_save_path)
    get_index_level_data(data_save_path)


if __name__ == "__main__":
    get_stock_and_index_data()
