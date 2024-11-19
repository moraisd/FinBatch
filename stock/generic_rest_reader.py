from config.config_reader import get_config
from rest import rest_api


@rest_api.get_data_dec
def get_stock_data(api, function, symbol):
    fundamental_data_api_config = get_config()["rest"]["fundamental_data_api"][api]
    return str((fundamental_data_api_config["url"])
               .replace('$function', function)
               .replace('$symbol', symbol)
               .replace('$key', fundamental_data_api_config["key"]))
