BEGIN;

INSERT INTO "listing_status" (
  "listing_status_id",
  "listing_status",
  "created_at",
  "created_by",
  "updated_at",
  "updated_by"
) VALUES
  (1, 'ACTIVE', NOW(), 'system', NOW(), 'system'),
  (2, 'INACTIVE', NOW(), 'system', NOW(), 'system');

COMMIT;