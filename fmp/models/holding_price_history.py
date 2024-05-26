import typing

from fmp.models.price_info import PriceInfo


class HoldingPriceHistory:
    def __init__(self, symbol: str, price_history: typing.List[PriceInfo]):
        self.symbol = symbol
        self.price_history = price_history

    @staticmethod
    def from_json(json_dictionary):
        def _from_json_price_history(price_history: dict) -> typing.List[PriceInfo]:
            price_info_list = []
            for history in price_history:
                info = PriceInfo(
                    history["date"],
                    history["open"],
                    history["high"],
                    history["low"],
                    history["close"],
                    history["adjClose"],
                    history["volume"],
                    history["unadjustedVolume"],
                    history["change"],
                    history["changePercent"],
                    history["vwap"],
                    history["label"],
                    history["changeOverTime"],
                )

                price_info_list.append(info)

            return price_info_list

        return HoldingPriceHistory(
            json_dictionary["symbol"],
            _from_json_price_history(json_dictionary["historical"]),
        )
