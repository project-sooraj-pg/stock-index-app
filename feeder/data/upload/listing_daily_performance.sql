BEGIN;

INSERT INTO postgres.public.listing_daily_performance (
    listing_id,
    trade_date,
    open_price,
    high_price,
    low_price,
    close_price,
    trade_volume,
    created_at,
    created_by,
    updated_at,
    updated_by
)
SELECT
    listing_id,
    trade_date,
    open_price,
    high_price,
    low_price,
    close_price,
    trade_volume,
    created_at,
    created_by,
    updated_at,
    updated_by
FROM listing_daily_performance;

COMMIT;

