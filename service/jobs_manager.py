import datetime as dt

from apscheduler.events import EVENT_JOB_EXECUTED
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config.config_reader import get_config
from service.stock_service import update_symbols, update_stocks

_scheduler = BlockingScheduler()
_executions_counter = 0


def run_and_schedule_symbol_job():
    _scheduler.add_job(update_symbols, IntervalTrigger(days=1), next_run_time=dt.datetime.utcnow())


def run_and_schedule_update_stocks_job():
    _scheduler.add_job(update_stocks, IntervalTrigger(minutes=1), id='update_stock')


def add_listeners():
    _scheduler.add_listener(_schedule_listener, EVENT_JOB_EXECUTED)


def _schedule_listener(event):
    # TODO Implement preserving job execution counter between Screener executions
    if event.job_id == 'update_stock':
        global _executions_counter
        _executions_counter += 1
        if _executions_counter == _max_executions_per_day():
            job = _scheduler.get_job(event.job_id)
            job.reschedule(IntervalTrigger(minutes=1, start_date=_next_day()))
            _executions_counter = 0


def _max_executions_per_day():
    fundamental_data_api = get_config()['rest']['fundamental_data_api']
    return fundamental_data_api['requests_per_day'] / fundamental_data_api['requests_per_minute']


def _next_day():
    return dt.datetime.utcnow() + dt.timedelta(days=1)


def run_jobs():
    _scheduler.start()
