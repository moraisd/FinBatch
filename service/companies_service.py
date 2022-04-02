from api.restapi import RestApi
from dao.companies_dao import CompaniesDao
from db.mongo_db import database
from service.csv_file_reader import CsvFileReader


class CompaniesService:
    def __init__(self, companies_dao: CompaniesDao = CompaniesDao(database),
                 csv_reader: CsvFileReader = CsvFileReader(),
                 rest_api: RestApi = RestApi(), config=None) -> None:
        if config is None:
            config = {}
        self.companies_dao = companies_dao
        self.csv_reader = csv_reader
        self.rest_api = rest_api
        self.config = config
        super().__init__()

    def update_tickers(self):
        listed_stocks = self.rest_api.request_get_data(
            f'{self.config["rest"]["ticker_api_url"]}{self.config["exchange_list"][0]}'
            f'?api_token={self.config["rest"]["ticker_api_key"]}')

        ticker_list = self.csv_reader.read_first_column(listed_stocks.text)

        database_ticker_list = self.companies_dao.find_all_tickers()

        return [tickers for tickers in ticker_list or database_ticker_list]
