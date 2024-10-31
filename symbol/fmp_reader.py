import fmpsdk

from config.config_reader import get_config


def read():
    # Free account limited to US Stock Exchange only
    return [symbol_info for symbol_info in fmpsdk.symbols_list(get_config()['rest']['symbol_api']['fmp']['key']) if
            symbol_info.get('type') == 'stock' and symbol_info.get('exchangeShortName') in {'CBOE', 'NASDAQ', 'NYSE',
                                                                                            'AMEX', 'BSE'}]
