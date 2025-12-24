## Backend Fast API Documentation

### Requirements
* A running instance postgres database with expected schema of the parent project (stock-index-app)
* A running instance of redis cache

### How to execute
* Create a virtual environment or use Poetry
* Use requirements.txt or pyproject.toml to ensure the dependencies

#### Using Poetry
```sh
poetry install
poetry run uvicorn app.app:app --reload
```

#### Using Python
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python uvicorn app.app:app --reload
```

#### Environment Variables
* Create a `.env` file in the project root to set environment variables.
* The application will automatically load variables from `.env` if `python-dotenv` is installed.

#### Required Environment Variables

The following environment variables must be set (typically in your `.env` file):

| Variable               | Description                          |
|------------------------|--------------------------------------|
| `POSTGRES_DB_USER`     | Postgres database owner username     |
| `POSTGRES_DB_PASSWORD` | Postgres database owner password     |
| `POSTGRES_DB`          | Postgres database name               |
| `POSTGRES_DB_HOST`     | Postgres database host               |
| `POSTGRES_DB_PORT`     | Postgres database port               |
| `REDIS_HOST`           | Redis server host                    |
| `REDIS_PORT`           | Redis server port                    |
| `INDEX_BASE_VALUE`     | Index base value (float)             |
| `TOTAL_NUMBER_OF_INDEX_CONSTITUENTS` | Total number of index constituents (int) |

Example `.env` file:

```
POSTGRES_DB_USER=your_username
POSTGRES_DB_PASSWORD=your_password
POSTGRES_DB=your_db_name
POSTGRES_DB_HOST=localhost
POSTGRES_DB_PORT=5432
REDIS_HOST=0.0.0.0
REDIS_PORT=6379
INDEX_BASE_VALUE=1000.0
TOTAL_NUMBER_OF_INDEX_CONSTITUENTS=100
```
