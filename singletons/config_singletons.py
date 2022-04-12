import logging.config

from config.config_reader import ConfigReader

reader = ConfigReader().read

config = reader("config.yaml")

logging.config.dictConfig(reader('logging.yaml'))
