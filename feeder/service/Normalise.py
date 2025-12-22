from typing import List

from feeder.utility.Configuration import Configuration
from feeder.utility.DuckDB import DuckDB
from feeder.utility.Logger import Logger


class Normalise:
    __logger = Logger.get_logger()
    __configuration = Configuration.load_from_file()

    @classmethod
    def normalize_tables(cls) -> None:
        """Method to normalise raw tables and store back in duckdb"""
        cls.__logger.info('normalising tables')
        normalisation_queries = cls.__get_normalisation_scripts()
        for normalisation_query in normalisation_queries:
            DuckDB.execute_query(normalisation_query)
        cls.__logger.info('normalisation completed')

    @classmethod
    def __get_normalisation_scripts(cls) -> List[str]:
        """Method to parse normalisation queries"""
        normalisation_queries = list()
        cls.__logger.info('obtaining normalisation queries...')
        normalisation_query_files = cls.__configuration['normalise']['queries']
        for normalisation_query_file in normalisation_query_files:
            with open(f'data/normalisation/{normalisation_query_file}', 'r') as file:
                normalisation_query = file.read()
            normalisation_queries.append(normalisation_query)
        cls.__logger.info('obtained')
        return normalisation_queries