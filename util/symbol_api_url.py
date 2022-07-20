from config.config_reader import get_config
from rest import rest_api


@rest_api.get_data_dec
def from_api(api: str):
    symbol_api_config = get_config()['rest']['symbol_api'][api]
    return (symbol_api_config['url']).replace('$key', symbol_api_config['key'])
