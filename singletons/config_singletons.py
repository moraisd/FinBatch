import logging.config
import os

from config.config_reader import ConfigReader

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

read = ConfigReader().read

config = read("config.yaml")

logging.config.dictConfig(read('logging.yaml'))
