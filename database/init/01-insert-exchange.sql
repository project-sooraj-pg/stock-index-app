BEGIN;

INSERT INTO "exchange" (
  "exchange_id",
  "exchange_code",
  "exchange_name",
  "exchange_description",
  "created_at",
  "created_by",
  "updated_at",
  "updated_by"
) VALUES
  (1, 'XNYS', 'New York Stock Exchange', 'The New York Stock Exchange (NYSE) is the largest stock exchange in the world by market capitalization of its listed companies.', NOW(), 'system', NOW(), 'system');

COMMIT;