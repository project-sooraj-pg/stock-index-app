BEGIN;

INSERT INTO "constituent_change_type" (
  "constituent_change_type_code",
  "constituent_change_type_description",
  "created_at",
  "created_by",
  "updated_at",
  "updated_by"
) VALUES
  ('ADDED', 'Added to the index constituents', NOW(), 'system', NOW(), 'system'),
  ('REMOVED', 'Removed from the index constituents', NOW(), 'system', NOW(), 'system');

COMMIT;