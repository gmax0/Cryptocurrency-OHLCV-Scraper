import datetime as DT

exchange_functions = {}

def register(func):
    exchange_functions[func.__name__] = func
    return func

@register
def binance_candle_mapping(candle):
    entry = {
        "open_timestamp" : int(candle[0]),
        "open" : float(candle[1]),
        "high" : float(candle[2]),
        "low" : float(candle[3]),
        "close" : float(candle[4]),
        "volume" : float(candle[5])
    }
    return entry

@register
def binance_us_candle_mapping(candle):
    entry = {
        "open_timestamp" : int(candle[0]),
        "open" : float(candle[1]),
        "high" : float(candle[2]),
        "low" : float(candle[3]),
        "close" : float(candle[4]),
        "volume" : float(candle[5])
    }
    return entry

@register
def coinbase_pro_candle_mapping(candle):
    entry = {
        "open_timestamp" : int(candle[0]) * 1000,
        "open" : candle[3],
        "high" : candle[2],
        "low" : candle[1],
        "close" : candle[4],
        "volume" : candle[5]
    }
    return entry

@register 
def ftx_candle_mapping(candle):
    entry = {
        "open_timestamp" : int(DT.datetime.strptime(candle['startTime'], "%Y-%m-%dT%H:%M:%S+00:00").replace(tzinfo=DT.timezone.utc).timestamp() * 1000),
        "open" : candle['open'],
        "high" : candle['high'],
        "low" : candle['low'],
        "close" : candle['close'],
        "volume" : candle['volume']
    }
    return entry

@register
def gemini_candle_mapping(candle):
    entry = {
        "open_timestamp" : candle[0],
        "open" : candle[1],
        "high" : candle[2],
        "low" : candle[3],
        "close" : candle[4],
        "volume" : candle[5]
    }
    return entry

@register
def kucoin_candle_mapping(candle):
    entry = {
        "open_timestamp" : int(DT.datetime.utcfromtimestamp(int(candle[0])).replace(tzinfo=DT.timezone.utc).timestamp() * 1000),
        "open" : float(candle[1]),
        "high" : float(candle[3]),
        "low" : float(candle[4]),
        "close" : float(candle[2]),
        "volume" : float(candle[5])
    }
    return entry