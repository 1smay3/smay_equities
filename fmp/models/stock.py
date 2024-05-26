class Stock:
    def __init__(self, symbol, exchange, exchange_short_name, price, name):
        self.symbol = symbol
        self.exchange = exchange
        self.exchange_short_name = exchange_short_name
        self.price = price
        self.name = name

    def __str__(self):
        return f"Stock(symbol={self.symbol}, exchange={self.exchange}, exchangeShortName={self.exchange_short_name}, price={self.price}, name={self.name})"
