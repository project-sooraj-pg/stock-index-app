# API Design Specification

## Controller And Endpoints
### Index Construction Controller (path: api/v1/IndexConstructionController.py)
The controller should have the following endpoints
POST: api/v1/build_index
Should accept two query parameters
1) start_date - date string of format 'YYYY-MM-DD' - mandatory
2) end_date - date string of format 'YYYY-MM-DD' - optional

Should return HTTP 201, created
Should return HTTP 500, on internal server error
Should return model {
  "base_date": "2025-08-04",
  "base_value": 1000,
  "rows_inserted": 250,
  "status": "completed"
}
when unable to process request return status accordingly

### Index Retrieval Controller (path api/v1/IndexRetrievalController.py)
The controller should have the following endpoints

GET /index-
performance?start_date=&end_date=
Return daily returns and cumulative returns
(cached).

GET /index-composition?date= Return 100-stock composition for a given
date (cached).

GET /composition-
changes?start_date=&end_date=
List days when composition changed, with
stocks entered/exited (cached).

### Data Export Controller (path: api/v1/DataExportController.py)
POST /export-data
o Export:
* Index performance in one sheet
* Daily compositions in second sheet
* Composition changes in third sheet
o Format: Excel (.xlsx) with clean headers and numeric formatting.

The API should have two repositories. One to access Postgres Database
The second One to Access Redis Cache

I should have One, or Two services to write the business logic.

The API Should Use Fast APi and should follow the best practises 

The api/v1/build index is going to call two stored procedures we created the index in the database

The endpoints of Index Retrieval Controller (path api/v1/IndexRetrievalController.py) should either execute queries 
which are stored part of the API code or I should create the views in database and Create model with Pydantic model validations

The API should have a swagger endpoint with proper documentation



