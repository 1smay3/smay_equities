import pandas as pd

from data.data_store import DataStore


def _infer_trade_direction(value: str) -> int:
    if "Purchase" in value:
        return 1
    elif "Sale" in value:
        return -1
    else:
        return 0


def convert_trades_to_impulses(datastore_oject: DataStore) -> pd.DataFrame:
    data = datastore_oject.SingleStock.senate_trading

    impulses_data = []
    for symbol, symbol_data in data.items():
        symbol_data["direction"] = symbol_data["type"].apply(_infer_trade_direction)

        impulses_frame = symbol_data.groupby(["dateRecieved"])[["direction"]].sum()
        impulses_frame.index = pd.to_datetime(impulses_frame.index)
        impulses_frame = impulses_frame.reindex(pd.date_range(impulses_frame.index[0], impulses_frame.index[-1], freq="B"))
        impulses_frame.columns = [symbol]
        impulses_data.append(impulses_frame)

    return pd.concat(impulses_data, axis=1)
