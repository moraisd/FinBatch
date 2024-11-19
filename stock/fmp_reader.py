import logging

import fmpsdk

from config.config_reader import get_config

_log = logging.getLogger(__name__)


def read(symbol):
    fmp_key = get_config()['rest']['fundamental_data_api']['fmp']['key']

    _log.info(f'Retrieving company profile from FMP for symbol: {symbol}')
    company_profile = fmpsdk.company_profile(fmp_key, symbol)

    if not company_profile:
        return {'symbol': symbol}

    _log.info(f'Retrieving TTM key metrics from FMP for symbol: {symbol}')
    ttm_fundamental_metrics = fmpsdk.key_metrics_ttm(fmp_key, symbol)

    if not ttm_fundamental_metrics:
        return company_profile[0]

    _log.info(f'Retrieving annual key metrics from FMP for symbol: {symbol}')
    annual_fundamental_metrics = fmpsdk.key_metrics(fmp_key, symbol)

    if not annual_fundamental_metrics:
        return company_profile[0] | {'ttmFundamentalMetrics': ttm_fundamental_metrics[0]}

    return company_profile[0] | {'ttmFundamentalMetrics': ttm_fundamental_metrics[0],
                                 'annualFundamentalMetrics': annual_fundamental_metrics}
