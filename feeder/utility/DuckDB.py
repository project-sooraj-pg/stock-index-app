import os
import json
import shutil

import duckdb

from typing import List

from feeder.utility.Logger import Logger

class DuckDB:
    __connection = None
    __logger = Logger.get_logger()
    __local_database_path = 'data/duckdb/database/database.duckdb'
    __local_json_storage_path = 'data/duckdb/json'

    @classmethod
    def __get_connection(cls):
        """Method to create and reuse connections"""
        if cls.__connection is None:
            cls.__logger.info(f'connecting to duckdb at {cls.__local_database_path}')
            cls.__connection = duckdb.connect(cls.__local_database_path)
        cls.__logger.info('connected')
        return cls.__connection

    @classmethod
    def close_connection(cls):
        """Method to close connection"""
        if cls.__connection is not None:
            cls.__logger.info('closing duckdb connection')
            cls.__connection.close()
            cls.__connection = None

    @classmethod
    def wipe_existing_data(cls):
        """Method to wipe data associated with duckdb"""
        try:
            for item in os.listdir('data/duckdb'):
                item_path = os.path.join('data/duckdb', item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
        except Exception as exception:
            cls.__logger.exception(exception)

    @classmethod
    def __store_data_as_json(cls, table_name: str, data: List[dict]) -> str:
        """Method to store the given data as json"""
        file_path = os.path.join(cls.__local_json_storage_path, f'{table_name}.json')
        cls.__logger.info(f'storing given data in: {file_path}')
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(json.dumps(data, indent=2))
            cls.__logger.info('stored successfully')
        except Exception as exception:
            file_path = None
            cls.__logger.error('storing data as json failed')
            cls.__logger.exception(exception)
        return file_path

    @classmethod
    def __store_data_into_duckdb(cls, table_name: str, json_file_path: str) -> None:
        """Method to store a given json file into duckdb"""
        if json_file_path:
            connection = cls.__get_connection()
            try:
                cls.__logger.info(f'storing given data in duckdb table: {table_name}')
                connection.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_json_auto(?)", [json_file_path])
                cls.__logger.info('stored successfully')
            except Exception as exception:
                cls.__logger.exception(exception)

        else:
            cls.__logger.error('unable to find relevant json file to persist into duckdb')

    @classmethod
    def save_data(cls, table_name: str, data: List[dict]) -> None:
        """Method to save data"""
        if not data:
            cls.__logger.warning('no data provided to save.')
            return None
        cls.__logger.info('saving data')
        json_file_path = cls.__store_data_as_json(table_name, data)
        cls.__store_data_into_duckdb(table_name, json_file_path)
        cls.__logger.info(f'saved {len(data)} records into {table_name}')

    @classmethod
    def execute_query(cls, query: str) -> List[dict]:
        """Method to execute query in duckdb"""
        connection = cls.__get_connection()
        cls.__logger.info('executing query in duckdb')
        cls.__logger.debug(f'query: {query}')
        cursor = connection.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]
        cls.__logger.info(f'results obtained: number of items: {len(results)}')
        return results
