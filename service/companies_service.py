from api.restapi import RestApi
from dao.companies_dao import CompaniesDao
from db.mongo_db import database
from service.csv_file_reader import CsvFileReader


class CompaniesService:
    def __init__(self, companies_dao: CompaniesDao = CompaniesDao(database),
                 csv_reader: CsvFileReader = CsvFileReader(),
                 rest_api: RestApi = RestApi()) -> None:
        self.companies_dao = companies_dao
        self.csv_reader = csv_reader
        self.rest_api = rest_api
        super().__init__()

    def update_tickers(self, config):
        ticker_data = self.rest_api.request_get_data(
            f'{config["rest"]["ticker_api_url"]}{config["exchange_list"][0]}'
            f'?api_token={config["rest"]["ticker_api_key"]}')

        ticker_list = self.csv_reader.read_first_column(ticker_data.text)

        database_ticker_list = self.companies_dao.find_all_tickers()

        lambda t_l: self.companies_dao.update_one(t_l, t_l)()
