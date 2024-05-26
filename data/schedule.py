"""Static mappings for what data to gather for each instrument type, to make it easy
to get new fields for new instruments when extending functionality later on"""

from fmp import fmp_data

# Mapping that defines what data to pull for what filters
single_stock_data_mapping = {
    "spx": ["historic_price_full"],
    # "nasdaq": ["historic_price_full"],
}

index_level_data_mapping = {"historic_price_full": ["spx_pr", "spx_tr"]}

index_level_symbol_mapping = {"spx_pr": "^GSPC", "spx_tr": "^SP500TR"}


data_name_to_endpoint_mapping = {
    "spx_latest_only": "sp500_constituent",
    "spx": "historical/sp500_constituent",
    # "nasdaq_latest": "nasdaq_constituent",
    # "nasdaq": "/historical/nasdaq_constituent",
}

map_field_name_to_function = {"historic_price_full": fmp_data.gather_simple_prices}
