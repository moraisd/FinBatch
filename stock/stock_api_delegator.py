from stock import fmp_reader


def get_from(api, symbol):
    match api:
        case 'fmp':
            return fmp_reader.read(symbol)
        case _:
            raise RuntimeError(f'No support for API named {api} found!')


def get_max_requests(config):
    total = 0
    apis = config['rest']['fundamental_data_api']
    for api in apis:
        total += apis[api]['requests_per_day']
    return total
