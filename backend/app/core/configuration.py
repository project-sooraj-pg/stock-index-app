from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()

class Configuration(BaseSettings):
    app_name: str = "stock-index-app"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""

configuration = Configuration()