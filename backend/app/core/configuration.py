from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()

class Configuration(BaseSettings):
    app_name: str = "stock-index-app"
    debug: bool = False
    postgres_db_owner: str = ""
    postgres_db_owner_password: str = ""
    postgres_db: str = ""
    redis_host: str = ""
    redis_port: int = ""
    index_base_value: float = 1000.0
    total_number_of_index_constituents: int = 100

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_db_owner}:{self.postgres_db_owner_password}@localhost:5432/{self.postgres_db}"

configuration = Configuration()