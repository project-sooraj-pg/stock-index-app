BEGIN;

INSERT INTO "listing_status" (
  "listing_status_code",
  "listing_status",
  "created_at",
  "created_by",
  "updated_at",
  "updated_by"
) VALUES
  ('A', 'ACTIVE', NOW(), 'system', NOW(), 'system'),
  ('I', 'INACTIVE', NOW(), 'system', NOW(), 'system');

COMMIT;