import logging.config
import os

from config.config_reader import ConfigReader

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

read = ConfigReader().read

config = read(os.path.join(ROOT_DIR, "config.yaml"))

logging.config.dictConfig(read(os.path.join(ROOT_DIR, 'logging.yaml')))
