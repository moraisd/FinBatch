from dao.companies_dao import CompaniesDao
from db.mongo_db import MongoDb
from service.companies_service import CompaniesService
from singletons.config_singletons import config

database = MongoDb(config).get_database(config['db']['database'])

companies_dao = CompaniesDao(database)

companies_service = CompaniesService(config, companies_dao)
