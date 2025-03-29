import asyncio
import logging
from asyncio import CancelledError

from scheduler.jobs_manager import (schedule_symbol_job, run_jobs, add_listeners,
                                    schedule_update_stocks_job)

_log = logging.getLogger(__name__)

async def main():
    schedule_symbol_job()
    schedule_update_stocks_job()
    add_listeners()
    run_jobs()
    await asyncio.Event().wait()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, CancelledError):
        _log.info('Application stopped')
