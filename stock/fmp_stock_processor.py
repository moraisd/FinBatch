def fix_annual_fundamental_data_from_fmp(annual_fundamental_metrics):
    for metrics in annual_fundamental_metrics:
        metrics['researchAndDevelopmentToRevenue'] = metrics.pop('researchAndDdevelopementToRevenue')
    return annual_fundamental_metrics


def fix_ttm_data_from_fmp(ttm_fundamental_metrics):
    for metrics in ttm_fundamental_metrics:
        metrics['researchAndDevelopmentToRevenueTTM'] = metrics.pop('researchAndDevelopementToRevenueTTM')
    return ttm_fundamental_metrics
