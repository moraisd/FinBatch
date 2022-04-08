import logging

from api.restapi import RestApi
from dao.companies_dao import CompaniesDao
from service.csv_file_reader import EodCsvFileReader


class CompaniesService:
    def __init__(self, config: dict, companies_dao: CompaniesDao,
                 csv_reader: EodCsvFileReader = EodCsvFileReader(),
                 rest_api: RestApi = RestApi()) -> None:
        self.companies_dao = companies_dao
        self.csv_reader = csv_reader
        self.rest_api = rest_api
        self.config = config
        super().__init__()

    def update_tickers(self):
        listed_stocks = self.rest_api.request_get_data(
            f'{self.config["rest"]["ticker_api"]["url"]}{self.config["exchange_list"][0]}'
            f'?api_token={self.config["rest"]["ticker_api"]["key"]}')

        ticker_set = self.csv_reader.retrieve_tickers(listed_stocks.text)
        database_ticker_set = self.companies_dao.find_all_tickers()

        new_tickers = ticker_set - database_ticker_set
        delisted_tickers = database_ticker_set - ticker_set

        logging.info(f'Number of tickers to be inserted: {len(new_tickers)}')
        self.companies_dao.insert_tickers(new_tickers)

        logging.info(f'Number of tickers to be delisted: {len(delisted_tickers)}')
        self.companies_dao.delete_delisted(delisted_tickers)

    # def update_stocks(self):
