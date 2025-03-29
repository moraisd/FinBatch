import asyncio
import logging

from scheduler.jobs_manager import (schedule_symbol_job, run_jobs, add_listeners,
                                    schedule_update_stocks_job, scheduler_shutdown)


async def main():
    schedule_symbol_job()
    schedule_update_stocks_job()
    add_listeners()
    run_jobs()


if __name__ == '__main__':
    asyncio.run(main())

