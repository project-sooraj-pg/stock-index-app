from feeder.service.Gather import Gather

from utility.Logger import Logger

class Feeder:
    __logger = Logger.get_logger()

    @classmethod
    def execute(cls):
        cls.__logger.info('starting application')
        try:
            Gather.gather_data()
        except Exception as exception:
            cls.__logger.exception(exception)
        cls.__logger.info('application exit')

if __name__ == '__main__':
    Feeder.execute()