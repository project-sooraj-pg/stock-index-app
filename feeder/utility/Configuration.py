import yaml

from feeder.utility.Logger import Logger

class Configuration:
    __configuration = None
    __logger = Logger.get_logger()

    @classmethod
    def load_from_file(cls):
        if cls.__configuration:
            return cls.__configuration
        with open('configuration/configuration.yaml', 'r') as file:
            configuration = yaml.safe_load(file)
        cls.__logger.info('starting application....')
        cls.__logger.info(f"active environment: {configuration['active']}")
        cls.__configuration = configuration[configuration['active']]
        return cls.__configuration
