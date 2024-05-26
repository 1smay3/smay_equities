"""Centralised Static variables, currently just to limit the API calls given the rate limit"""

import os

from utils.extensions import double_backslash_to_slash

COUNT_API_MAX_CALLS = 100
TIME_LIMIT_COOLDOWN_SECONDS = 60
PRETTY_INDEX_NAME = {"sp500_constituent": "spx"}

PRICE_FIELD_NAME = "historic_price_full"


def get_project_root_path() -> str:
    return os.path.dirname(double_backslash_to_slash(str(__file__)))


COLOUR_PALLETTE_HEX = ["#2EC4B6", "#CBF3F0", "#FFBF69", "#FF9F1C"]

ANNUAL_TRADING_DAYS = 260
