from config.config_reader import config
from service.companies_service import CompaniesService

# response = rest_api.request_get_data(
#     f'{rest_config["fundamental_data_url"]}?{ApiParameters.DATA_TYPE}=OVERVIEW&{ApiParameters.TICKER}=GOOG'
#     f'&apikey={rest_config["fundamental_data_key"]}')
#
# companies_dao = CompaniesDao(database)
# companies_dao.insert_one(response.json())
#
# print(companies_dao.find_one('GOOG'))

if __name__ == '__main__':

    CompaniesService().update_tickers()
