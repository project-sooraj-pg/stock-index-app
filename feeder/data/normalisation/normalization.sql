--- create company table
CREATE OR REPLACE TABLE company AS
WITH aggregated_data AS (
    SELECT DISTINCT
        COALESCE(t.cik, o.cik) AS cik,
        t.name AS company_name,
        o.description AS company_description,
        t.locale AS country_code,
        o.homepage_url AS website,
        o.data_date::DATE AS shares_outstanding_as_of_date,
        o.share_class_shares_outstanding AS shares_outstanding,
        o.market_cap AS adjusted_market_capitalization,
        t.primary_exchange AS exchange_code,
        t.ticker AS ticker_symbol,
        p."from"::DATE AS trade_date,
        p.open AS open_price,
        p.high AS high_price,
        p.low AS low_price,
        p.close AS close_price,
        p.volume AS volume
    FROM ticker t
    LEFT JOIN ticker_overview o
        ON t.ticker = o.ticker
    LEFT JOIN ticker_price p
        ON t.ticker = p.symbol
)
SELECT DISTINCT
    CAST(cik AS BIGINT) AS company_id,
    UPPER(company_name) AS company_name,
    company_description,
    UPPER(country_code) AS country_code,
    website,
    NOW() AS created_at,
    'feeder' AS created_by,
    NOW() AS updated_at,
    'feeder' AS updated_by
FROM aggregated_data
WHERE cik IS NOT NULL;

--- create company_shares_outstanding table
CREATE OR REPLACE TABLE company_shares_outstanding AS
WITH aggregated_data AS (
    SELECT DISTINCT
        COALESCE(t.cik, o.cik) AS cik,
        t.name AS company_name,
        o.description AS company_description,
        t.locale AS country_code,
        o.homepage_url AS website,
        o.data_date::DATE AS shares_outstanding_as_of_date,
        o.share_class_shares_outstanding AS shares_outstanding,
        o.market_cap AS adjusted_market_capitalization,
        t.primary_exchange AS exchange_code,
        t.ticker AS ticker_symbol,
        p."from"::DATE AS trade_date,
        p.open AS open_price,
        p.high AS high_price,
        p.low AS low_price,
        p.close AS close_price,
        p.volume AS volume
    FROM ticker t
    LEFT JOIN ticker_overview o
        ON t.ticker = o.ticker
    LEFT JOIN ticker_price p
        ON t.ticker = p.symbol
)
SELECT DISTINCT
    CAST(cik AS BIGINT) AS company_id,
    shares_outstanding_as_of_date AS effective_date,
    shares_outstanding,
    NOW() AS created_at
FROM aggregated_data
WHERE shares_outstanding IS NOT NULL;

--- create listing table
CREATE OR REPLACE TABLE listing AS
WITH aggregated_data AS
    (SELECT DISTINCT
        COALESCE(t.cik, o.cik) AS cik,
        t.name AS company_name,
        o.description AS company_description,
        t.locale AS country_code,
        o.homepage_url AS website,
        o.data_date:: DATE AS shares_outstanding_as_of_date,
        o.share_class_shares_outstanding AS shares_outstanding,
        o.market_cap AS adjusted_market_capitalization,
        t.primary_exchange AS exchange_code,
        t.ticker AS ticker_symbol,
        p."from"::DATE AS trade_date,
        p.open AS open_price,
        p.high AS high_price,
        p.low AS low_price,
        p.close AS close_price,
        p.volume AS volume
    FROM ticker t
    LEFT JOIN ticker_overview o
        ON t.ticker = o.ticker
    LEFT JOIN ticker_price p
        ON t.ticker = p.symbol
    )
SELECT
    ROW_NUMBER() OVER (ORDER BY ticker_symbol) AS listing_id,
    CAST(cik AS BIGINT) AS company_id,
    1 AS exchange_id,
    ticker_symbol,
    1 AS listing_status_id,
    NOW() AS created_at,
    'feeder' AS created_by,
    NOW() AS updated_at,
    'feeder' AS updated_by
FROM (
    SELECT DISTINCT ticker_symbol, cik
    FROM aggregated_data
) x;

CREATE OR REPLACE TABLE listing_daily_performance AS
WITH aggregated_data AS
    (SELECT DISTINCT
        COALESCE(t.cik, o.cik) AS cik,
        t.name AS company_name,
        o.description AS company_description,
        t.locale AS country_code,
        o.homepage_url AS website,
        o.data_date:: DATE AS shares_outstanding_as_of_date,
        o.share_class_shares_outstanding AS shares_outstanding,
        o.market_cap AS adjusted_market_capitalization,
        t.primary_exchange AS exchange_code,
        t.ticker AS ticker_symbol,
        p."from"::DATE AS trade_date,
        p.open AS open_price,
        p.high AS high_price,
        p.low AS low_price,
        p.close AS close_price,
        p.volume AS volume
    FROM ticker t
    LEFT JOIN ticker_overview o
        ON t.ticker = o.ticker
    LEFT JOIN ticker_price p
        ON t.ticker = p.symbol
    )
SELECT
    l.listing_id,
    f.trade_date,
    f.open_price,
    f.high_price,
    f.low_price,
    f.close_price,
    f.volume,
    NOW() AS created_at
FROM aggregated_data f
JOIN listing l
    ON f.ticker_symbol = l.ticker_symbol
WHERE f.trade_date IS NOT NULL;

