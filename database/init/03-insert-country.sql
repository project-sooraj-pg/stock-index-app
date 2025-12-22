BEGIN;

INSERT INTO "country" (
  "country_code",
  "country_name",
  "created_at",
  "created_by",
  "updated_at",
  "updated_by"
) VALUES
  ('US', 'USA', NOW(), 'system', NOW(), 'system');

COMMIT;