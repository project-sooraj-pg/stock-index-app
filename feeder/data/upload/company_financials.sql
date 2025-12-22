BEGIN;

INSERT INTO postgres.public.company_financials (
    company_id,
    financial_date,
    shares_outstanding,
    market_cap,
    created_at,
    created_by,
    updated_at,
    updated_by
)
SELECT
    company_id,
    financial_date,
    shares_outstanding,
    market_cap,
    created_at,
    created_by,
    updated_at,
    updated_by
FROM company_financials;

COMMIT;

