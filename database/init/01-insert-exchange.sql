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
  (1, 'NYSE', 'New York Stock Exchange', 'The New York Stock Exchange (NYSE) is the largest stock exchange in the world by market capitalization of its listed companies.', NOW(), 'system', NOW(), 'system'),
  (2, 'NASDAQ', 'NASDAQ Stock Market', 'The NASDAQ Stock Market is an American stock exchange located in New York City, known for its high concentration of technology companies.', NOW(), 'system', NOW(), 'system'),
  (3, 'LSE', 'London Stock Exchange', 'The London Stock Exchange (LSE) is one of the world''s oldest stock exchanges and is located in London, England.', NOW(), 'system', NOW(), 'system'),
  (4, 'JPX', 'Japan Exchange Group', 'The Japan Exchange Group (JPX) is a financial services corporation that operates multiple securities exchanges including the Tokyo Stock Exchange.', NOW(), 'system', NOW(), 'system'),
  (5, 'SSE', 'Shanghai Stock Exchange', 'The Shanghai Stock Exchange (SSE) is one of the two stock exchanges operating independently in the People''s Republic of China.', NOW(), 'system', NOW(), 'system');

COMMIT;