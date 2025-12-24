BEGIN;

--- create normalized company table
CREATE OR REPLACE TABLE company AS
SELECT
    company_id,
    company_name,
    company_description,
    country_code,
    website,
    NOW() AS created_at,
    'feeder' AS created_by,
    NOW() AS updated_at,
    'feeder' AS updated_by
FROM (
    SELECT
        CAST(o.cik AS BIGINT) AS company_id,
        ANY_VALUE(o.name) AS company_name,
        ANY_VALUE(o.description) AS company_description,
        ANY_VALUE(UPPER(o.locale)) AS country_code,
        ANY_VALUE(o.homepage_url) AS website
    FROM ticker_overview o
    WHERE o.cik IS NOT NULL
    GROUP BY o.cik
);

--- create listing table
CREATE OR REPLACE TABLE listing AS
WITH ranked AS (
    SELECT
        ROW_NUMBER() OVER (
            PARTITION BY t.cik
            ORDER BY t.ticker ASC
        ) AS rn,

        CAST(t.cik AS BIGINT) AS company_id,
        t.ticker AS ticker_symbol,
        t.type AS listing_type_code,
        t.active
    FROM ticker t
    INNER JOIN company c
        ON t.cik = c.company_id
    WHERE t.cik IS NOT NULL
)
SELECT
    ROW_NUMBER() OVER (ORDER BY ticker_symbol) AS listing_id,
    company_id,
    1 AS exchange_id,
    ticker_symbol,
    listing_type_code,
    CASE
        WHEN active = true THEN 'A'
        ELSE 'I'
    END AS listing_status_code,
    NOW() AS created_at,
    'feeder' AS created_by,
    NOW() AS updated_at,
    'feeder' AS updated_by
FROM ranked
WHERE rn = 1;

--- create listing_daily_performance table
CREATE OR REPLACE TABLE listing_daily_performance AS
SELECT DISTINCT
    l.listing_id,
    p."from"::DATE AS trade_date,
    p.open AS open_price,
    p.high AS high_price,
    p.low AS low_price,
    p.close AS close_price,
    p.volume AS trade_volume,
    NOW() AS created_at,
    'feeder' AS created_by,
    NOW() AS updated_at,
    'feeder' AS updated_by
FROM ticker_price p
JOIN listing l
    ON p.symbol = l.ticker_symbol
WHERE p."from" IS NOT NULL;

--- create listing_market_cap_change
CREATE OR REPLACE TABLE  listing_market_cap_change AS
WITH overview_with_listing AS (
    SELECT
        l.listing_id,
        t.data_date::DATE AS change_date,
        t.market_cap
    FROM ticker_overview t
    JOIN listing l
        ON t.ticker = l.ticker_symbol
    WHERE t.market_cap IS NOT NULL
),
ranked_changes AS (
    SELECT
        *,
        LAG(market_cap) OVER (PARTITION BY listing_id ORDER BY change_date) AS prev_market_cap
    FROM overview_with_listing
)
SELECT
    listing_id,
    change_date,
    market_cap,
    NOW() AS created_at,
    'feeder' AS created_by,
    NOW() AS updated_at,
    'feeder' AS updated_by
FROM ranked_changes
WHERE prev_market_cap IS NULL       -- first valid value
   OR market_cap <> prev_market_cap
ORDER BY listing_id, change_date;

COMMIT;
