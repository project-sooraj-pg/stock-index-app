BEGIN;

INSERT INTO "ranking_method" (
  "ranking_method_code",
  "ranking_method_description",
  "created_at",
  "created_by",
  "updated_at",
  "updated_by"
) VALUES
  ('MARKET_CAP', 'Ranking by Market Capitalization', NOW(), 'system', NOW(), 'system');

COMMIT;