import logging

from singletons.app_singletons import companies_service

if __name__ == '__main__':
    log = logging.getLogger(__name__)

    log.info("Updating tickers")
    companies_service.update_tickers()
    log.info("Finished updating tickers")

    log.info("Updating stock data")
    companies_service.update_stocks()
    log.info("Finished updating stock data")
