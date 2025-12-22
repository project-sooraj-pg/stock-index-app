from utility.Logger import Logger
from feeder.utility.Parser import Parser

from feeder.service.Gather import Gather
from feeder.service.Upload import Upload
from feeder.service.Normalise import Normalise

class Feeder:
    __logger = Logger.get_logger()

    @classmethod
    def execute(cls):
        cls.__logger.info('starting application')
        try:
            # fetch data from origin - polygon.io (if origin trigger is enabled)
            origin_trigger = Parser.get_origin_trigger()
            if origin_trigger:
                Gather.gather_data(override_previous=True)
            # normalise data - will replace the normalised tables
            Normalise.normalize_tables()
            # upload data to postgres
            Upload.reload_tables_in_postgres()
        except Exception as exception:
            cls.__logger.exception(exception)
        cls.__logger.info('application exit')

if __name__ == '__main__':
    Feeder.execute()