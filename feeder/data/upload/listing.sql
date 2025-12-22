BEGIN;

INSERT INTO postgres.public.listing (
    listing_id,
    company_id,
    exchange_id,
    ticker_symbol,
    listing_type_code,
    listing_status_code,
    created_at,
    created_by,
    updated_at,
    updated_by
)
SELECT
    listing_id,
    company_id,
    exchange_id,
    ticker_symbol,
    listing_type_code,
    listing_status_code,
    created_at,
    created_by,
    updated_at,
    updated_by
FROM listing;

COMMIT;

