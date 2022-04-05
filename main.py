import logging

from singletons.config_singletons import companies_service

if __name__ == '__main__':
    logging.info("Starting ticker update service")
    companies_service.update_tickers()
