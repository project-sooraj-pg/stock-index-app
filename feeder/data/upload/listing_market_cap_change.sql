BEGIN;

INSERT INTO postgres.public.listing_market_cap_change (
    listing_id,
    change_date,
    market_cap,
    created_at,
    created_by,
    updated_at,
    updated_by
)
SELECT
    listing_id,
    change_date,
    market_cap,
    created_at,
    created_by,
    updated_at,
    updated_by
FROM listing_market_cap_change;

COMMIT;

