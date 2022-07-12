import os
from unittest import TestCase

import config.config_reader as config_reader


class TestConfig(TestCase):

    def test_read_config(self):
        config = config_reader._read_yaml(
            os.path.join(config_reader.get_root_dir(), os.path.dirname(__file__), 'test_config.yaml'))

        self.assertDictEqual(config, {'rest': {'base_url': 'https://www.alphavantage.co/query',
                                               'data_type': 'function',
                                               'symbol': 'AAPL',
                                               'api_key': 'apikey'
                                               }})
