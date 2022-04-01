import yaml


class ConfigReader:
    def read(self, url):
        with open(url, 'r') as file:
            return yaml.safe_load(file)


config = ConfigReader().read("config.yaml")
