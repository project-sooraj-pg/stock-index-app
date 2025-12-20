BEGIN;

INSERT INTO "exchange_performance_metric" (
  "exchange_performance_metric_id",
  "exchange_performance_metric_description",
  "performance_metric_id",
  "exchange_id",
  "created_at",
  "created_by",
  "updated_at",
  "updated_by"
) VALUES
  (1, 'Close price in NYSE', 1, 1, NOW(), 'system', NOW(), 'system');

COMMIT;