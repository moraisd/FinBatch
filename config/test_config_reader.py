import os
from unittest import TestCase

from config.config_reader import ConfigReader
from singletons.config_singletons import ROOT_DIR


class TestConfig(TestCase):

    def test_read_config(self):
        config = ConfigReader().read(os.path.join(ROOT_DIR, os.path.dirname(__file__), 'test_config.yaml'))

        self.assertDictEqual(config,
                             {'rest':
                                  {'base_url': 'https://www.alphavantage.co/query',
                                   'data_type': 'function',
                                   'ticker': 'symbol',
                                   'api_key': 'apikey'
                                   }})
