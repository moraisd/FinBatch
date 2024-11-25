import logging

_log = logging.getLogger(__name__)


def process(stock):
    if stock.get('ttmFundamentalMetrics'):
        stock['ttmFundamentalMetrics'] = _fix_ttm_fundamental_data_from_fmp(stock['ttmFundamentalMetrics'])
    if stock.get('annualFundamentalMetrics'):
        stock['annualFundamentalMetrics'] = _fix_annual_fundamental_data_from_fmp(stock['annualFundamentalMetrics'])
    return stock


def _fix_annual_fundamental_data_from_fmp(annual_fundamental_metrics):
    for metrics in annual_fundamental_metrics:
        try:
            metrics['researchAndDevelopmentToRevenue'] = metrics.pop('researchAndDdevelopementToRevenue')
        except KeyError:
            _log.info('Could not find "researchAndDdevelopementToRevenue". Typo possibly fixed upstream')

    return annual_fundamental_metrics


def _fix_ttm_fundamental_data_from_fmp(ttm_fundamental_metrics: dict):
    try:
        ttm_fundamental_metrics['researchAndDevelopmentToRevenueTTM'] = ttm_fundamental_metrics.pop(
            'researchAndDevelopementToRevenueTTM')
    except KeyError:
        _log.info('Could not find "researchAndDevelopementToRevenueTTM". Typo possibly fixed upstream')

    return ttm_fundamental_metrics
