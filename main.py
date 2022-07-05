from singletons.app_singletons import jobs_scheduler

if __name__ == '__main__':
    jobs_scheduler.run_and_schedule_ticker_job()
    jobs_scheduler.run_and_schedule_update_stocks_job()
    jobs_scheduler.add_listeners()
    jobs_scheduler.run_jobs()
