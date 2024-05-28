import polars as pl
import arcticdb as adb

class ArcticHandler:
    def __init__(self, local_arctic_path: str):
        self.local_arctic_path = local_arctic_path
        self.arctic_instance = adb.Arctic(f"lmdb:///{self.local_arctic_path}?map_size=20GB")

    def create_arctic_library(self, library_name: str):
        self.arctic_instance.create_library(library_name)

    def save_dataframe_to_arctic(self, arctic_library_name: str, data: pl.DataFrame, symbol: str):
        arctic_library = self.arctic_instance[arctic_library_name]

        # Note: Converting straight into pandas for now, as Arctic doesn't support Polars yet.
        arctic_library.write(symbol, data.to_pandas())