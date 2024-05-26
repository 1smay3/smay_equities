import arcticdb as adb
import polars as pl
from data.data_cache.definitions import LOCAL_ARCTIC_PATH

def save_dataframe_to_arctic(
   arctic_library_name:str, data: pl.DataFrame, symbol: str
):
    arctic_instance = adb.Arctic(f"lmdb:///{LOCAL_ARCTIC_PATH}?map_size=20GB")
    arctic_library = arctic_instance[arctic_library_name]

    # Note: Converting straight into pandas for now, as Arctic doesnt
    # support polars yet.

    arctic_library.write(symbol, data.to_pandas())


def _create_arctic_library(local_arctic_path:str, library_name):
    ac = adb.Arctic(f"lmdb:///{local_arctic_path}?map_size=20GB")
    ac.create_library(library_name)


