BEGIN;

INSERT INTO postgres.public.company (
    company_id,
    company_name,
    company_description,
    country_code,
    website,
    created_at,
    created_by,
    updated_at,
    updated_by
)
SELECT
    company_id,
    company_name,
    company_description,
    country_code,
    website,
    created_at,
    created_by,
    updated_at,
    updated_by
FROM company;

COMMIT;