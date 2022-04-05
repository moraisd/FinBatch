from config.config_reader import ConfigReader
from dao.companies_dao import CompaniesDao
from db.mongo_db import MongoDb
from service.companies_service import CompaniesService

config = ConfigReader().read("config.yaml")

database = MongoDb(config).get_database(config['db']['database'])

companies_dao = CompaniesDao(database)

companies_service = CompaniesService(config, companies_dao)
