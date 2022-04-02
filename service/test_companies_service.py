from unittest import TestCase
from unittest.mock import Mock, MagicMock

from service.companies_service import CompaniesService


class CompaniesServiceTest(TestCase):

    def setUp(self) -> None:
        self.companies_service = CompaniesService(Mock(), Mock(), Mock(), MagicMock())
        super().setUp()

    def test_update_tickers(self):
        rest_data = ['AAPL', 'MSFT', 'AMZN', 'FB', 'V', 'VALE3']
        db_data = ['AAPL', 'MSFT', 'AMZN']

        self.companies_service.csv_reader.read_first_column.return_value = rest_data
        self.companies_service.companies_dao.find_all_tickers.return_value = db_data

        db_result = self.companies_service.update_tickers()

        self.assertListEqual(db_result, rest_data)
