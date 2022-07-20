from symbol import alphavantage_reader, eod_reader
from util.symbol_api_url import from_api


def get_from(api):
    match api:
        case 'alphavantage':
            return alphavantage_reader.read(from_api(api).text)
        case 'eodhistoricaldata':
            return eod_reader.read(from_api(api).text)
        case _:
            raise RuntimeError(f'No support for API named {api} found!')
