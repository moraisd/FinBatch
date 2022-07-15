import logging

_log = logging.getLogger(__name__)


def fetch_symbols(api):
    match api:
        case 'alphavantage':
            return alphavantage.get_symbols(api['alphavantage'])
        case 'eodhistoricaldata':
            return eodhistoricaldata.get_symbols(api['eodhistoricaldata'])
        case _:
            raise RuntimeError(f'No support for API named {api} found!')
