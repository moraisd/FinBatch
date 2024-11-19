import fmpsdk

from config.config_reader import get_config


def read():
    # Free account limited to US Stock Exchanges only
    return {symbol_info['symbol'] for symbol_info in
            fmpsdk.symbols_list(get_config()['rest']['symbol_api']['fmp']['key']) if
            symbol_info['type'] == 'stock' and symbol_info['exchangeShortName'] in {'CBOE', 'NASDAQ', 'NYSE',
                                                                                    'AMEX'}}
