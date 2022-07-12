from service.jobs_manager import (run_and_schedule_symbol_job, run_and_schedule_update_stocks_job, add_listeners,
                                  run_jobs)

if __name__ == '__main__':
    run_and_schedule_symbol_job()
    run_and_schedule_update_stocks_job()
    add_listeners()
    run_jobs()
