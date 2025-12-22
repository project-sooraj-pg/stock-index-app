BEGIN;

INSERT INTO "listing_type" (
  "listing_type_code",
  "listing_type_name",
  "created_at",
  "created_by",
  "updated_at",
  "updated_by"
) VALUES
  ('CS', 'Common Stock', NOW(), 'system', NOW(), 'system');

COMMIT;