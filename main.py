import asyncio

from scheduler.jobs_manager import (schedule_symbol_job, run_jobs, add_listeners,
                                    schedule_update_stocks_job, scheduler_shutdown)


async def main():
    schedule_symbol_job()
    schedule_update_stocks_job()
    add_listeners()
    run_jobs()
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except (KeyboardInterrupt, Exception):
        # Gracefully shut down on Ctrl+C
        print("\nShutting down scheduler...")
        scheduler_shutdown()
        loop.stop()
        print("Scheduler and event loop stopped.")


if __name__ == '__main__':
    asyncio.run(main())
