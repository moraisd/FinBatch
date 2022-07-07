import logging.config
import os

import yaml


def get_config():
    return _config


def get_root_dir():
    return _ROOT_DIR


def _read_yaml(url):
    with open(url, 'r') as file:
        return yaml.safe_load(file)


_ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

_config = _read_yaml(os.path.join(_ROOT_DIR, "config.yaml"))

logging.config.dictConfig(_read_yaml(os.path.join(_ROOT_DIR, 'logging.yaml')))
