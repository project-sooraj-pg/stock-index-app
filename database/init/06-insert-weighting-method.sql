BEGIN;

INSERT INTO "weighting_method" (
  "weighting_method_code",
  "weighting_method_description",
  "created_at",
  "created_by",
  "updated_at",
  "updated_by") VALUES
   ('EQUAL', 'Equal weightage for all constituents', NOW(), 'system', NOW(), 'system');

COMMIT;