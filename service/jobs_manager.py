import datetime as dt

from apscheduler.events import EVENT_JOB_EXECUTED
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger


class JobManager:
    def __init__(self, config, companies_service):
        self._config = config
        self._companies_service = companies_service
        self._executions_counter = 0
        self._sched = BlockingScheduler()

    def run_and_schedule_ticker_job(self):
        self._sched.add_job(self._companies_service.update_tickers,
                            IntervalTrigger(days=1), next_run_time=dt.datetime.now())

    def run_and_schedule_update_stocks_job(self):
        self._sched.add_job(self._companies_service.update_stocks,
                            IntervalTrigger(minutes=1), id='update_stock')

    def add_listeners(self):
        self._sched.add_listener(self.__schedule_listener, EVENT_JOB_EXECUTED)

    def __schedule_listener(self, event):
        # TODO Implement preserving job execution counter between Screener executions

        if event.job_id == 'update_stock':
            self._executions_counter += 1
            if self._executions_counter == self.__max_executions_per_day():
                job = self._sched.get_job(event.job_id)
                job.reschedule(IntervalTrigger(minutes=1, start_date=self.__next_day()))
                self._executions_counter = 0

    def __max_executions_per_day(self):
        fundamental_data_api = self._config['rest']['fundamental_data_api']
        return fundamental_data_api['requests_per_day'] / fundamental_data_api['requests_per_minute']

    @staticmethod
    def __next_day():
        return dt.datetime.utcnow() + dt.timedelta(days=1)

    def run_jobs(self):
        self._sched.start()
