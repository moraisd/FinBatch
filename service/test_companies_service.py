from unittest import TestCase
from unittest.mock import Mock

from service.companies_service import CompaniesService


class CompaniesServiceTest(TestCase):

    def setUp(self) -> None:
        self.companies_service = CompaniesService(Mock(), Mock(), Mock())
        super().setUp()

    def test_update_tickers(self):
        rest_data = ['AAPL', 'MSFT', 'AMZN', 'FB', 'V', 'VALE3']
        db_data = ['AAPL', 'MSFT', 'AMZN', 'ABCD']

        self.companies_service.csv_reader.read_first_column.return_value = rest_data
        self.companies_service.companies_dao.find_all_tickers.return_value = db_data

        self.companies_service.update_tickers()

        companies_dao = self.companies_service.companies_dao

        companies_dao.insert_many.assert_called_once_with([{'Symbol': 'FB'}, {'Symbol': 'V'}, {'Symbol': 'VALE3'}])
        companies_dao.delete_delisted.assert_called_once_with(['ABCD'])
