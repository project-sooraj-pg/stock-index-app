import os

from feeder.utility.Configuration import Configuration
from feeder.utility.DuckDB import DuckDB
from feeder.utility.Logger import Logger


class Upload:

    __logger = Logger.get_logger()
    __configuration = Configuration.load_from_file()

    __database = os.environ.get("POSTGRES_DB")
    __user = os.environ.get("POSTGRES_DB_OWNER")
    __password = os.environ.get("POSTGRES_DB_OWNER_PASSWORD")
    __host = os.environ.get("POSTGRES_DB_HOST")
    __port = os.environ.get("POSTGRES_DB_PORT")

    @classmethod
    def reload_tables_in_postgres(cls) -> None:
        """Method to reload the given in postgres with the normalised table in duckdb"""
        table_names = cls.__configuration['upload']['table_names']
        cls.__attach_postgres_to_duckdb()
        for table_name in table_names:
            cls.__reload_table_in_postgres(table_name)
        cls.__detach_postgres_from_duckdb()

    @classmethod
    def __reload_table_in_postgres(cls, table_name) -> None:
        """Method to reload given table in postgres with normalised table in duckdb"""
        try:
            cls.__logger.info(f"reloading data in {table_name} in database: {cls.__database}")
            truncate_query = f"TRUNCATE TABLE {cls.__database}.public.{table_name}; "
            DuckDB.execute_query(truncate_query)
            insert_query = cls.__load_insert_query_from_file(table_name)
            DuckDB.execute_query(insert_query)
            cls.__logger.info("reload_completed")
        except Exception as exception:
            cls.__logger.exception(exception)

    @classmethod
    def __load_insert_query_from_file(cls, table_name):
        """Method to load insert query from file"""
        query = ""
        cls.__logger.info(f"loading data insert query fro table: {table_name}")
        try:
            query_file = f"data/upload/{table_name}.sql"
            with open(query_file, 'r') as file:
                query = file.read()
            cls.__logger.info("loaded query successfully")
        except Exception as exception:
            cls.__logger.exception(exception)
        return query

    @classmethod
    def __attach_postgres_to_duckdb(cls) -> None:
        """Method to attach postgres database to duckdb as a foreign database"""
        cls.__logger.info("attaching postgres to duckdb")
        try:
            postgres_credentials = f"""
                'dbname={cls.__database}
                user={cls.__user}
                password={cls.__password}
                host={cls.__host}
                port={cls.__port}
            """
            query = f"ATTACH {postgres_credentials} AS {cls.__database} (TYPE postgres);"
            DuckDB.execute_query(query)
            cls.__logger.info(f"postgres database {cls.__database} at {cls.__host}:{cls.__port} attached to duckdb")
        except Exception as exception:
            cls.__logger.exception(exception)

    @classmethod
    def __detach_postgres_from_duckdb(cls) -> None:
        """Method to detach postgres from duckdb"""
        cls.__logger.info(f"detaching postgres database (name:{cls.__database}) to duckdb")
        try:
            query = f"DETACH {cls.__database}"
            DuckDB.execute_query(query)
            cls.__logger.info(f"postgres database {cls.__database} detached from duckdb")
        except Exception as exception:
            cls.__logger.exception(exception)
