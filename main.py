import logging

from singletons.config_singletons import companies_service

if __name__ == '__main__':
    logging.info("Starting ticker update service")
    companies_service.update_tickers()
    logging.info("Finished ticker update service")

    # logging.info("Starting fetching stock data")
    # companies_service.update_stocks()
    # logging.info("Finished fetching stock data")
