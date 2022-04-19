import datetime
import logging

from api.restapi import RestApi
from dao.companies_dao import CompaniesDao
from service.eod_csv_file_reader import EodCsvFileReader


class CompaniesService:

    def __init__(self, config: dict, companies_dao: CompaniesDao,
                 csv_reader: EodCsvFileReader = EodCsvFileReader(),
                 rest_api: RestApi = RestApi()) -> None:
        self.companies_dao = companies_dao
        self.csv_reader = csv_reader
        self.rest_api = rest_api
        self.config = config
        self.log = logging.getLogger(__name__)
        super().__init__()

    def update_tickers(self):

        ticker_set = set()
        for exchange in self.config['exchange_list']:
            listed_stocks = self.rest_api.request_get_data(self.__get_ticker_url(exchange))
            ticker_set |= self.csv_reader.retrieve_tickers(listed_stocks.text)

        database_ticker_set = self.companies_dao.find_all_tickers()

        new_tickers = ticker_set - database_ticker_set
        delisted_tickers = database_ticker_set - ticker_set

        new_tickers_total = len(new_tickers)
        if new_tickers_total:
            self.log.info(f'Number of tickers to be inserted: {new_tickers_total}')
            self.companies_dao.insert_tickers(new_tickers)

        delisted_tickers_total = len(delisted_tickers)
        if delisted_tickers_total:
            self.log.info(f'Number of tickers to be delisted: {delisted_tickers_total}')
            self.companies_dao.delete_delisted(delisted_tickers)

    def update_stocks(self):
        outdated_stocks_tickers = self.companies_dao.find_outdated_stocks(
            self.config["rest"]["fundamental_data_api"]["requests_per_minute"])

        self.log.info(f'Updating the following stock data: {outdated_stocks_tickers}')

        self.companies_dao.bulk_write(self.__retrieve_stocks_data(outdated_stocks_tickers))

    def __retrieve_stocks_data(self, outdated_stocks_tickers):
        stocks = []
        for ticker in outdated_stocks_tickers:
            stock: dict = self.rest_api.request_get_data(self.__build_stocks_data_url(ticker)).json()
            if stock.get('Symbol'):
                stock['LastUpdated'] = datetime.datetime.utcnow()
                stocks.append(self.companies_dao.prepare_update_one(ticker, stock))
            else:
                stocks.append(self.companies_dao.prepare_update_one(ticker, {'blacklisted': True}))
                # TODO Create job to remove brand new stocks from blacklist after first data retrieval
        return stocks

    def __get_ticker_url(self, exchange) -> str:
        return str(self.config['rest']['ticker_api']['url']).replace('$exchange', exchange).replace('$key',
                                                                                                    self.config['rest'][
                                                                                                        'ticker_api'][
                                                                                                        'key'])

    def __build_stocks_data_url(self, ticker):
        return str(self.config["rest"]["fundamental_data_api"]["url"]).replace('$function', 'OVERVIEW').replace(
            '$symbol', ticker).replace('$key', self.config["rest"]["fundamental_data_api"]["key"])
