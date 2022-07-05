import yaml


class ConfigReader:
    @staticmethod
    def read(url):
        with open(url, 'r') as file:
            return yaml.safe_load(file)
