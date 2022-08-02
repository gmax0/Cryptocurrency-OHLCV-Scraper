from py_cc_ohlcv import exchanges

# instrument_mapping: Apply this to the scraper's instrument symbol 
# timestamp_format: String or Int representing second multiplier operand (e.g. 1000 * seconds = milliseconds)
# response_keys: List of keys to traverse down a nested JSON structure received in the request response

exchange_metadata = {
    exchanges.BINANCE : {
        'instrument_mapping' : (lambda inst: ''.join(inst.split("_"))),
        'url' : "https://api.binance.com/api/v3/klines?symbol={}&interval={}&startTime={}&endTime={}&limit=1000",
        'timestamp_format' : 1000,
        'resolutions': {
            '1m': '1m',
            '5m': '5m',
            '15m': '15m',
            '1h': '1h',
            '6h': '6h',
            '1d': '1d'
        },
        'max_candles_per_req': 1000,
        'response_keys' : []
    },
    exchanges.BINANCE_US: {
        'instrument_mapping' : (lambda inst: ''.join(inst.split("_"))),
        'url' : "https://api.binance.us/api/v3/klines?symbol={}&interval={}&startTime={}&endTime={}&limit=1000",
        'timestamp_format' : 1000,
        'resolutions': {
            '1m': '1m',
            '5m': '5m',
            '15m': '15m',
            '1h': '1h',
            '6h': '6h',
            '1d': '1d'
        },
        'max_candles_per_req': 1000,
        'response_keys' : []
    },
    exchanges.BINANCE_FUTURES: {
        'instrument_mapping' : (lambda inst: ''.join(inst.split("_"))),
        'url' : "https://fapi.binance.com/fapi/v1/klines?symbol={}&interval={}&startTime={}&endTime={}&limit=1500",
        'timestamp_format' : 1000,
        'resolutions': {
            '1m': '1m',
            '5m': '5m',
            '15m': '15m',
            '1h': '1h',
            '6h': '6h',
            '1d': '1d'
        },
        'max_candles_per_req': 1000,
        'response_keys' : []
    },
    exchanges.COINBASE_PRO: {
        'instrument_mapping' : (lambda inst: '-'.join(inst.split("_"))),
        'url' : "https://api.exchange.coinbase.com/products/{}/candles?granularity={}&start={}&end={}",
        'timestamp_format' : "%Y-%m-%dT%H:%M:%S.%fZ",
        'resolutions': {
            '1m': 60,
            '5m': 300,
            '15m': 900,
            '1h': 3600,
            '6h': 21600,
            '1d': 86400
        },
        'max_candles_per_req': 300,
        'response_keys': []
    },
    exchanges.FTX: {
        'instrument_mapping' : (lambda inst: '/'.join(inst.split("_"))),
        'url' : "https://ftx.com/api/markets/{}/candles?resolution={}&start_time={}&end_time={}",
        'timestamp_format' : 1,
        'resolutions' : {
            '1m': 60
        },
        'max_candles_per_req': 300,
        'response_keys': ['result']
    },
    exchanges.GEMINI: {
        'instrument_mapping' : (lambda inst: ''.join(inst.split("_"))),
        'url' : "https://api.gemini.com/v2/candles/{}/{}",
        'timestamp_format' : 1000,
        'resolutions' : {
            '1m': '1m'
        },
        'max_candles_per_req': 300,
        'response_keys': []
    },
    exchanges.KUCOIN: {
        'instrument_mapping' : (lambda inst: '-'.join(inst.split("_"))),
        'url' : "https://api.kucoin.com/api/v1/market/candles?symbol={}&type={}&startAt={}&endAt={}",
        'timestamp_format' : 1,
        'resolutions': {
            '1m': '1min'
        },
        'max_candles_per_req': 300,
        'response_keys': ['data']
    }
}