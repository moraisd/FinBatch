from config.config_reader import ConfigReader
from unittest import TestCase


class TestConfig(TestCase):

    def test_read_config(self):
        config = ConfigReader().read('test_config.yaml')

        self.assertDictEqual(config,
                             {'rest':
                                  {'base_url': 'https://www.alphavantage.co/query',
                                   'data_type': 'function',
                                   'ticker': 'symbol',
                                   'api_key': 'apikey'
                                   }})
