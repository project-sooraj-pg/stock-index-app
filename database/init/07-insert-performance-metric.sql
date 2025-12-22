BEGIN;

INSERT INTO "performance_metric" (
   "performance_metric_id",
  "performance_metric_name",
  "created_at",
  "created_by",
  "updated_at",
  "updated_by"
) VALUES
  (1, 'Close Price', NOW(), 'system', NOW(), 'system');

COMMIT;