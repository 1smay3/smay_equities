import typing


class PriceInfo:
    def __init__(
        self,
        date,
        open_price,
        high,
        low,
        close,
        adj_close,
        volume,
        unadjusted_volume,
        change,
        change_percent,
        vwap,
        label,
        change_over_time,
    ):
        self.date = date
        self.open_price = open_price
        self.high = high
        self.low = low
        self.close = close
        self.adj_close = adj_close
        self.volume = volume
        self.unadjusted_volume = unadjusted_volume
        self.change = change
        self.change_percent = change_percent
        self.vwap = vwap
        self.label = label
        self.change_over_time = change_over_time

    def to_date_adj_close_dict(self) -> typing.Dict[str, str]:
        return {self.date: self.adj_close}

    def __str__(self):
        return f"PriceInfo(date={self.date}, open={self.open_price}, high={self.high}, low={self.low}, close={self.close}, adjClose={self.adj_close}, volume={self.volume}, unadjustedVolume={self.unadjusted_volume}, change={self.change}, changePercent={self.change_percent}, vwap={self.vwap}, label={self.label}, changeOverTime={self.change_over_time})"
