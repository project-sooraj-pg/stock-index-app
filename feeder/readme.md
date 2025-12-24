## Feeder Documentation

### Requirements
* Subscription to https://massive.io (old - polygon.io)
* A running instance postgres database with expected schema of the
  parent project (stock-index-app)

### Use Case
* Calls https://massive.io to fetch financial data as per the specifications 
provided in configuration/configuration.yaml
* Stores batchwise in duckdb - file located at data/duckdb/database/database.duckdb
* Normalise data by executing SQL query against stored data and creates tables which 
holds one to one mapping with the schema requirement of parent project.
* Uploads data into postgres database (ensure postgres instance is running before executing)

### How to execute
* Create a virtual environment or use Poetry
* Use requirements.txt or pyproject.toml to ensure the dependencies

#### Using Poetry
```sh
poetry install
# setting the argument as true will make the feeder fetch data from massive 
poetry run python Feeder.py --fetch_from_origin=true
# if set to false, data gathering will be disabled - existing data in duckdb will be used to normalise and upload
# idempotency is ensured - running multiple times is not expected to cause data corruption
poetry run python Feeder.py --fetch_from_origin=false
```

#### Using Python
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python Feeder.py --fetch_from_origin=false
```

#### Environment Variables
* Create a `.env` file in the project root to set environment variables.
* The application will automatically load variables from `.env` if `python-dotenv` is installed.

#### Required Environment Variables

The following environment variables must be set (typically in your `.env` file):

| Variable                      | Description                          |
|-------------------------------|--------------------------------------|
| `POSTGRES_DB_OWNER`           | Postgres database owner username     |
| `POSTGRES_DB_OWNER_PASSWORD`  | Postgres database owner password     |
| `POSTGRES_DB`                 | Postgres database name               |
| `POSTGRES_DB_HOST`            | Postgres database host               |
| `POSTGRES_DB_PORT`            | Postgres database port               |
| `API_KEY`                     | API key for massive.io (polygon.io)  |

Example `.env` file:

```
POSTGRES_DB_OWNER=your_username
POSTGRES_DB_OWNER_PASSWORD=your_password
POSTGRES_DB=your_db_name
POSTGRES_DB_HOST=localhost
POSTGRES_DB_PORT=5432
API_KEY=your_massive_io_api_key
```
