import polars as pl


def _filter_duplicate_columns_to_newest_and_longest(dataframe):
    """
    TODO
    NOTE: Likely not needed, but an FYI for the future
    For each column in a dataframe, remove any duplicate columns in the following hierachy:
    1. Choose the column with the most recent data point, irrespective of length
    2. Choose the column with the most amount of data by count
    3. Add a catch for same everything x
    """
    raise NotImplementedError


def sanity_clean_data(dataframe):
    """
    Apply cleaning to all timeseries dataframes - this cleaning is to standardise
    frames and help prevent any problems upstream and reduce repeated code. Any cleaning
    here works if applied to a dataframe thats alreadu cleaned
    """
    dataframe.index = pl.to_datetime(dataframe.index)
    dataframe = dataframe.sort_index()
    return dataframe
