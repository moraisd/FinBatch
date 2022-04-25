import time
from datetime import timedelta

import schedule

from singletons.app_singletons import companies_service
from singletons.config_singletons import config

if __name__ == '__main__':
    schedule.every(1).day.do(companies_service.update_tickers)
    stock_update_job = schedule.every(1).minute.do(companies_service.update_stocks).until(timedelta(
        minutes=config['rest']['fundamental_data_api']['requests_per_day'] / config['rest']['fundamental_data_api'][
            'requests_per_minute']))
    schedule.every(1).day.do(stock_update_job.run)

    while True:
        schedule.run_pending()
        time.sleep(schedule.idle_seconds())
