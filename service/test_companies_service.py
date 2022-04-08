from unittest import TestCase
from unittest.mock import Mock

from service.companies_service import CompaniesService


class CompaniesServiceTest(TestCase):

    def setUp(self) -> None:
        self.companies_service = CompaniesService(Mock(), Mock(), Mock())
        super().setUp()

    def test_update_tickers(self):
        rest_data = {'AAPL', 'MSFT', 'AMZN', 'FB', 'V', 'VALE3'}
        db_data = {'AAPL', 'MSFT', 'AMZN', 'ABCD'}

        self.companies_service.csv_reader.retrieve_tickers.return_value = rest_data
        self.companies_service.companies_dao.find_all_tickers.return_value = db_data

        self.companies_service.update_tickers()

        companies_dao = self.companies_service.companies_dao

        companies_dao.insert_tickers.assert_called_once_with({'V', 'VALE3', 'FB'})
        companies_dao.delete_delisted.assert_called_once_with({'ABCD'})

    # def test_update_stocks(self):
    #   rest_data = get_rest_Data()
