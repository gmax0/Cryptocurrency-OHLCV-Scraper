from py_cc_ohlcv import exchanges, instruments, symbols
from datetime import datetime

class Scraper:
    exchange = None
    instrument = None
    symbol = None

    url = None
    http_proxy = None
    window_start = None
    window_end = None

    def __init__(self, exchange, instrument, start_time, end_time):
        self.exchange = exchange
        self.instrument = instrument

        self.symbol = symbols.symbols_by_exchange[self.exchange][self.instrument] 
        print(self.symbol)

        self.window_start = start_time
        self.window_end = end_time

    def set_start(self, start_time: datetime):
        self.window_start = start_time

    def set_end(self, end_time: datetime):
        self.window_end = end_time

    def set_http_proxy(self, http_proxy: str):
        self.http_proxy = http_proxy

    