from api.restapi import RestApi
from config.config_reader import config
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
        self.config = config
        super().__init__()

    def update_tickers(self):
        listed_stocks = self.rest_api.request_get_data(
            f'{self.config["rest"]["ticker_api_url"]}{self.config["exchange_list"][0]}'
            f'?api_token={self.config["rest"]["ticker_api_key"]}')

        ticker_list = self.csv_reader.read_first_column(listed_stocks.text)

        database_ticker_list = self.companies_dao.find_all_tickers()
        new_tickers = [{'Symbol': ticker} for ticker in ticker_list if ticker not in database_ticker_list]
        delisted_tickers = [ticker for ticker in database_ticker_list if ticker not in ticker_list]

        self.companies_dao.insert_many(new_tickers)
        self.companies_dao.delete_delisted(delisted_tickers)
