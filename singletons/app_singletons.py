import dao.companies_dao as companies_dao
import rest.rest_api as rest_api
import service.eod_csv_file_reader as eod_reader
from config.config_reader import get_config
from service.companies_service import CompaniesService
from service.jobs_manager import JobManager

companies_service = CompaniesService(get_config(), companies_dao, rest_api, eod_reader)

jobs_scheduler = JobManager(get_config(), companies_service)
