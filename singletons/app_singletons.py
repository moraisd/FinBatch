from dao.companies_dao import CompaniesDao
from db.mongo_db import MongoDb
from rest.restapi import RestApi
from service.companies_service import CompaniesService
from service.jobs_aps import JobsAPS
from singletons.config_singletons import config

database = MongoDb(config).get_database(config['db']['database'])

companies_dao = CompaniesDao(database['companies'])

rest_api = RestApi()

companies_service = CompaniesService(config, companies_dao, rest_api)

jobs_scheduler = JobsAPS(config, companies_service)
