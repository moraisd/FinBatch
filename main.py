from scheduler.jobs_manager import (schedule_symbol_job, run_jobs, add_listeners,
                                    schedule_update_stocks_job)

if __name__ == '__main__':
    schedule_symbol_job()
    schedule_update_stocks_job()
    add_listeners()
    run_jobs()
