from flask import Flask

from rest.flask_blueprints import bp
from singletons.app_singletons import jobs_scheduler

if __name__ == '__main__':
    main_app = Flask(__name__)

    jobs_scheduler.run_and_schedule_ticker_job()
    jobs_scheduler.run_and_schedule_update_stocks_job()
    jobs_scheduler.run_jobs()

    main_app.register_blueprint(bp)
    main_app.run()
