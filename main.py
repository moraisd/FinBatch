from alphavantage.constants.apiparameters import ApiParameters
from api.restapi import rest_api
from config.config_reader import config
from dao.companies_dao import CompaniesDao
from db.mongo_db import database
from service.companies_service import companies_service

rest_config = config['rest']

companies_service.update_tickers(config)

# response = rest_api.request_get_data(
#     f'{rest_config["fundamental_data_url"]}?{ApiParameters.DATA_TYPE}=OVERVIEW&{ApiParameters.TICKER}=GOOG'
#     f'&apikey={rest_config["fundamental_data_key"]}')
#
# companies_dao = CompaniesDao(database)
# companies_dao.insert_one(response.json())
#
# print(companies_dao.find_one('GOOG'))
