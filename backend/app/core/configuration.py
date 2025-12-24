from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()

class Configuration(BaseSettings):
    # application configuration
    app_name: str = "stock-index-app"
    debug: bool = False
    # database configuration
    postgres_db_owner: str = ""
    postgres_db_owner_password: str = ""
    postgres_db: str = ""
    postgres_db_host: str =""
    postgres_db_port: int = 5432
    # cache configuration
    redis_host: str = ""
    redis_port: int = 6379
    # index -base value and total number of constituents configuration
    index_base_value: float = 1000.0
    total_number_of_index_constituents: int = 100

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_db_owner}:{self.postgres_db_owner_password}@{self.postgres_db_host}:{self.postgres_db_port}/{self.postgres_db}"

configuration = Configuration()