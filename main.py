import logging

from singletons.app_singletons import companies_service

if __name__ == '__main__':
    log = logging.getLogger(__name__)

    log.info("Starting ticker update service")
    companies_service.update_tickers()
    log.info("Finished ticker update service")

    # logging.info("Starting fetching stock data")
    # companies_service.update_stocks()
    # logging.info("Finished fetching stock data")
