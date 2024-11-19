from unittest import TestCase

from stock import fmp_processor


class StockFmpProcessorTest(TestCase):

    def setUp(self):
        self.fmp_processor = fmp_processor
        super().setUp()

    def test_fix_fundamental_data_from_fmp(self):
        stock = {'annualFundamentalMetrics': [{'researchAndDdevelopementToRevenue': 1234},
                                              {'researchAndDdevelopementToRevenue': 5678}],
                 'ttmFundamentalMetrics': {'researchAndDevelopementToRevenueTTM': 1234}
                 }

        result = self.fmp_processor.process(stock)

        self.assertDictEqual(result, {'annualFundamentalMetrics': [{'researchAndDevelopmentToRevenue': 1234},
                                                                   {'researchAndDevelopmentToRevenue': 5678}],
                                      'ttmFundamentalMetrics': {'researchAndDevelopmentToRevenueTTM': 1234}
                                      })

    def test_ignore_future_fixing_upstream_data(self):
        stock = {'ttmFundamentalMetrics': {'researchAndDevelopmentToRevenueTTM': 1234},
                 'annualFundamentalMetrics': [{'researchAndDevelopmentToRevenue': 1234},
                                              {'researchAndDevelopmentToRevenue': 5678}]}
        result = self.fmp_processor.process(stock)

        self.assertDictEqual(result, stock)

    def test_process_no_data(self):
        stock = {'symbol': 'SYMBOL'}
        result = self.fmp_processor.process(stock)

        self.assertEqual(result, stock)
