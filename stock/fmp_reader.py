import logging

import fmpsdk

from config.config_reader import get_config
from stock import fmp_stock_processor

_log = logging.getLogger(__name__)


def read(symbol):
    fmp_key = get_config()['rest']['fundamental_data_api']['fmp']['key']

    _log.info(f'Retrieving company profile from FMP for symbol: {symbol}')
    company_profile = fmpsdk.company_profile(fmp_key, symbol)

    if not company_profile:
        return None

    _log.info(f'Retrieving TTM key metrics from FMP for symbol: {symbol}')
    ttm_fundamental_metrics = fmpsdk.key_metrics_ttm(fmp_key, symbol)

    _log.info(f'Retrieving annual key metrics from FMP for symbol: {symbol}')
    annual_fundamental_metrics = fmpsdk.key_metrics(fmp_key, symbol)

    if ttm_fundamental_metrics and annual_fundamental_metrics:
        ttm_fundamental_metrics = fmp_stock_processor.fix_ttm_data_from_fmp(ttm_fundamental_metrics)
        annual_fundamental_metrics = fmp_stock_processor.fix_annual_fundamental_data_from_fmp(
            annual_fundamental_metrics)
        return {'ttmFundamentalMetrics': ttm_fundamental_metrics[0],
                'annualFundamentalMetrics': annual_fundamental_metrics} | company_profile[0]
    else:
        return None
