"""
Handles calls to the FMP API, returning a List[str] or Any representing the response
"""

import typing
from functools import partial
from typing import List

from fmpsdk.url_methods import __return_json_v3

from fmp.models.constituent import Constituent
from fmp.models.stock import Stock
from repository.async_job import AsyncJob
from repository.config import fmp_api_service_config as config
from repository.config.fmp_api_service_config import GET_HISTORIC_PRICES
from utils.extensions import T, map_list, safe_list

DATA_FROM_DATE = "1900-01-01"  # Rarely does any data go back this far, but this is to ensure we get all avaialbe data from the API


def get_historic_prices(symbol_list) -> List[dict]:
    def symbol_to_list(symbol: str) -> str:
        return f"{GET_HISTORIC_PRICES}{symbol}?from={DATA_FROM_DATE}"

    paths = map_list(symbol_list, symbol_to_list)
    return _call_fmp_multiple(paths)


def get_constituents(symbol: str) -> list[Constituent]:
    result = _call_fmp_single(symbol)

    def result_to_constituent(network_result) -> Constituent:
        return Constituent(network_result["symbol"])

    constituents_list: list[Constituent] = []
    for (
        constituent
    ) in result:  # TODO: Need to do this automatically by matching param names.
        constituent = Constituent(
            constituent["symbol"]
        )  # TODO: Need more flexibility to do symbol only or more detialed
        constituents_list.append(constituent)

    return constituents_list


def get_constituents_no_survivorship_bias(symbol: str) -> list[Constituent]:
    result = _call_fmp_single(symbol)
    constituents_list: list[Constituent] = []
    for (
        constituent
    ) in result:  # TODO: Need to do this automatically by matching param names.
        constituent = Constituent(constituent["symbol"])
        constituents_list.append(constituent)

    return constituents_list


def get_stock_list() -> typing.List[Stock]:
    return _call_fmp_single(config.GET_STOCK_LIST)


# May call directly (from this file).
def _call_fmp_multiple(paths: typing.List[str]) -> typing.List[dict]:
    def path_to_partial_call(endpoint: str) -> partial:
        return _partial_fmp_call(endpoint)

    constructed_network_calls = map_list(paths, path_to_partial_call)

    job = AsyncJob(constructed_network_calls)
    results = job.execute_tasks()
    return results  # A JSON Array again.


# May call directly (from this file).
def _call_fmp_single(path: str) -> typing.List:
    return _safe_fmp_call(path)


# Do not call directly.
def _partial_fmp_call(path: str) -> partial:
    return partial(_safe_fmp_call, path)


# Do not call directly.
def _safe_fmp_call(path: str) -> typing.List[T]:
    query_vars = {"apikey": config.API_KEY}
    # Strictly speaking we "shouldn't" call directly here. But we need better control than the library provides atm.
    result = __return_json_v3(path=path, query_vars=query_vars)
    print(f"Finished call to {path}")
    return safe_list(result)
