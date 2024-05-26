import arcticdb as adb
import pandas as pd#
from data.data_cache.definitions import LOCAL_ARCTIC_PATH

def save_dataframe_to_arctic(
   arctic_library_name:str, data: pd.DataFrame, symbol: str
):
    arctic_instance = adb.Arctic(f"lmdb:///{LOCAL_ARCTIC_PATH}?map_size=20GB")
    arctic_library = arctic_instance[arctic_library_name]
    arctic_library.write(symbol, data)


def _create_arctic_library(local_arctic_path:str, library_name):
    ac = adb.Arctic(f"lmdb:///{local_arctic_path}?map_size=20GB")
    ac.create_library(library_name)


