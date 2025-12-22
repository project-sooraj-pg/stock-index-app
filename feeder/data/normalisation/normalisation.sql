BEGIN;

--- create normalized company table
CREATE OR REPLACE TABLE company AS
SELECT DISTINCT
    CAST(COALESCE(t.cik, o.cik) AS BIGINT) AS company_id,
    UPPER(t.name) AS company_name,
    o.description AS company_description,
    UPPER(t.locale) AS country_code,
    o.homepage_url AS website,
    NOW() AS created_at,
    'feeder' AS created_by,
    NOW() AS updated_at,
    'feeder' AS updated_by
FROM ticker t
LEFT JOIN ticker_overview o
    ON t.ticker = o.ticker
WHERE COALESCE(t.cik, o.cik) IS NOT NULL;

--- create normalized company_daily_financials table
CREATE OR REPLACE TABLE company_financials AS
SELECT
    company_id,
    financial_date,
    shares_outstanding,
    market_cap,
    NOW() AS created_at,
    'feeder' AS created_by,
    NOW() AS updated_at,
    'feeder' AS updated_by
FROM (
    SELECT
        CAST(o.cik AS BIGINT) AS company_id,
        o.data_date::DATE AS financial_date,
        o.share_class_shares_outstanding AS shares_outstanding,
        o.market_cap AS market_cap,

        LAG(o.share_class_shares_outstanding) OVER (
            PARTITION BY o.cik
            ORDER BY o.data_date
        ) AS prev_shares_outstanding,

        LAG(o.market_cap) OVER (
            PARTITION BY o.cik
            ORDER BY o.data_date
        ) AS prev_market_cap
    FROM ticker_overview o
    WHERE o.cik IS NOT NULL
      AND o.data_date IS NOT NULL
)
WHERE
    -- first ever record for the company
    prev_shares_outstanding IS NULL
    AND prev_market_cap IS NULL

    -- OR any meaningful change
    OR shares_outstanding IS DISTINCT FROM prev_shares_outstanding
    OR market_cap IS DISTINCT FROM prev_market_cap;

--- create listing table
CREATE OR REPLACE TABLE listing AS
SELECT
    ROW_NUMBER() OVER (ORDER BY t.ticker) AS listing_id,
    CAST(t.cik AS BIGINT) AS company_id,
    1 AS exchange_id,
    t.ticker AS ticker_symbol,
    t.type AS listing_type_code,
    CASE
        WHEN t.active = true THEN 'A'
        ELSE 'I'
    END AS listing_status_code,
    NOW() AS created_at,
    'feeder' AS created_by,
    NOW() AS updated_at,
    'feeder' AS updated_by
FROM ticker t
WHERE t.cik IS NOT NULL;

--- create listing_daily_performance table
CREATE OR REPLACE TABLE listing_daily_performance AS
SELECT
    l.listing_id,
    p."from"::DATE AS trade_date,
    p.open AS open_price,
    p.high AS high_price,
    p.low AS low_price,
    p.close AS close_price,
    p.volume,
    NOW() AS created_at
FROM ticker_price p
JOIN listing l
    ON p.symbol = l.ticker_symbol
WHERE p."from" IS NOT NULL;

COMMIT;

