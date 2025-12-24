# Stock Index App
This is a backend service that tracks and manages a custom equal-weighted stock
index comprising the top 100 (configurable in env variable) US stocks by daily market capitalization.
The index is computed in such a way that each stock maintains an equal notional weight and is updated daily
to reflect market cap changes and to rebalance composition.

## How to run the Application

Install Poetry
```bash
pip install poetry
```

Install Docker
```bash
brew install --cask docker
```

Go to root directory of the project
```bash
cd /path/to/project/root
```

Create .env in the root directory with the variables given below

| Variable Name                      | Description                        | Example Value          |
|------------------------------------|------------------------------------|------------------------|
| POSTGRES_DB_USER                   | Postgres DB user                   | db-owner               |
| POSTGRES_DB_PASSWORD               | Postgres DB password               | db-owner-password      |
| POSTGRES_DB                        | Name of the Postgres database      | postgres               |
| POSTGRES_DB_HOST                   | Host for Postgres DB               | 0.0.0.0                |
| POSTGRES_DB_PORT                   | Port for Postgres on host machine  | 5432                   |
| POSTGRES_DB_PERSISTENCE_VOLUME     | Postgres data persistence volume   | ./database/data/server |
| PGADMIN_PORT                       | Port for pgAdmin                   | 5050                   |
| PGADMIN_DEFAULT_EMAIL              | Default email for pgAdmin          | admin@admin.com        |
| PGADMIN_DEFAULT_PASSWORD           | Default password for pgAdmin       | admin                  |
| PGADMIN_PERSISTENCE_VOLUME         | pgAdmin data persistence volume    | ./database/data/client |
| REDIS_HOST                         | Redis host                         | redis                  |
| REDIS_PORT                         | Redis port                         | 6379                   |
| INDEX_BASE_VALUE                   | Index base value                   | 1000.0                 |
| TOTAL_NUMBER_OF_INDEX_CONSTITUENTS | Total number of index constituents | 100                    |

Create .env for feeder. Refer to: [Feeder README](feeder/readme)

Run the whole application in Docker
```bash
docker compose --env-file .env up -d
```

If this is your first time, go to the feeder directory and execute feeder with fetch_from_origin flag set to false

Note: The committed DuckDB contains more than a month's data, which can be inserted quickly into PostgreSQL with the command below
```bash
cd feeder
poetry run feeder --fetch_from_origin=false
```

## Useful Curl Commands

### 1. Export index data as Excel file
```bash
curl -X POST \
  http://localhost:8000/api/v1/export-data \
  -H "Content-Type: application/json" \
  -d '{"index_code": "SP100", "start_date": "2025-01-01", "end_date": "2025-12-01"}'
```

### 2. Build index with given parameters
```bash
curl -X POST \
  http://localhost:8000/api/v1/build_index \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2025-01-01", "end_date": "2025-12-01"}'
```

### 3. Get index performance data (list)
```bash
curl -X GET "http://localhost:8000/api/v1/index-performance?index_code=SP100&start_date=2025-01-01&end_date=2025-12-01" -H "accept: application/json"
```

### 4. Get index composition data (list)
```bash
curl -X GET "http://localhost:8000/api/v1/index-composition?index_code=SP100&trade_date=2025-12-01" -H "accept: application/json"
```

### 5. Get index composition changes (list)
```bash
curl -X GET "http://localhost:8000/api/v1/composition-changes?index_code=SP100&start_date=2025-01-01&end_date=2025-12-01" -H "accept: application/json"
```

## Tech Stacks Used
* Python
* FastAPI
* Redis
* DuckDB
* Pandas
* Docker (with docker-compose)

## Components
The application has four major components

### 1) Feeder
Feeder is a standalone job which connects with https://massive.io (polygon.io in the past) APIs. More specifically, 
it connects to three endpoints given below:

| Sl. No. | API Endpoint                                         | Purpose                                        |
|---------|------------------------------------------------------|------------------------------------------------|
| 1       | https://api.massive.com/v3/reference/tickers         | Fetch ticker by exchange code                  |
| 2       | https://api.massive.com/v3/reference/tickers{ticker} | Fetch market cap and company details           |
| 3       | https://api.massive.com/v1/open-close                | Fetch daily price data for each ticker by date |

This standalone job is highly configurable to asynchronously fetch data from different date ranges, exchanges, and other filters 
permitted by the source. As the limit is five API calls per minute, it is recommended to use a paid subscription. The feeder uses DuckDB to store 
JSON responses received from the API as is—this is processed in batchwise and can be configured. After gathering the data, a normalization 
query is executed in DuckDB to create normalized tables. These normalized tables hold a one-to-one mapping with the original intended data model,
but lack referential integrity constraints and other checks. After normalization, DuckDB directly attaches to the PostgreSQL database to perform the ingestion. Hence, a PostgreSQL instance must be running while running Feeder. For more details, refer to: [Feeder README](feeder/readme.md)

### 2) PostgreSQL Database
PostgreSQL is used as the master database with a solid relational model. 
The  [Data Model Diagram](doc/datamodel/datamodel.pdf) and DBML file can be found [here](doc/datamodel). 
DB Diagram.io is used to generate the data model and schema. The business logic of the application is also within PostgreSQL as views and functions. This choice is for performance, simplicity of the API, and data quality.

### 3) FastAPI (Backend Service)
FastAPI is used to build the service to interact with PostgreSQL. The API allows creation of indexes, fetching 
index performance information, and also allows exporting generated data into Excel. The details of the endpoints are given below:

| Sl. No. | API Endpoint         | Method | Purpose/Description                                 |
|---------|----------------------|--------|-----------------------------------------------------|
| 1       | /export-data         | POST   | Export index data as Excel file                     |
| 2       | /build_index         | POST   | Build index with given parameters                   |
| 3       | /index-performance   | GET    | Get index performance data (list)                   |
| 4       | /index-composition   | GET    | Get index composition data (list)                   |
| 5       | /composition-changes | GET    | Get index composition changes (list)                |

For more details, refer to the component-specific documentation: [Backend README](backend/readme.md)

### 4) Redis Cache
Redis Cache is used to cache the API calls to speed up the response, and its usage is minimal and straightforward.

## Architecture
![architecture.png](doc/architecture.png)

## Production And Scaling Improvements
To make this whole application work as a system, all four components need to work together:
* Feeder as a daily scheduled job
* PostgreSQL, Redis, FastAPI as services

Hence, the following improvements can be considered:

1) As of now, the feeder is created to truncate the table and reload the data. This must be changed to a 
reconciliation process which inserts only the records that are not available in the database. Luckily, the design 
of the feeder application permits such enrichment of features. Hence, adding reconciliation 
will be one possible improvement. 
2) The feeder already uses a configurable loop to fetch data from the API and persist into DuckDB. However, 
the normalization will happen only after all the data is persisted into DuckDB. This is a limitation. A more ideal 
choice would be to gather, normalize, and ingest into PostgreSQL in a batchwise loop.
3) The index data is synchronized at the table level. That means, in the current setup, multiple users cannot create
and analyze indexes. Because the data persisted for one index would be overridden by the next index creation. 
For the purpose of the application, this is chosen intentionally to have idempotency in every operation. 
In order to achieve multiple indexes, each created index should have an ID and selected configurations for that index—i.e., ranking method, weighting method, rebalance schedule, etc. And each of these specifications must map to 
generalized PostgreSQL functions which can be assembled to form a particular index.

Apart from these, the design choices of the feeder, API directory structures, asynchronous nature, the choice of delegating normalization to DuckDB, choice of data model, and the choice of delegating computational complexity to PostgreSQL functions are very friendly for further extension and scalability.
