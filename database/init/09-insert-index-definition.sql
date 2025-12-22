BEGIN;

INSERT INTO "index_definition" (
  "index_definition_id",
  "index_code",
  "index_name",
  "index_description",
  "base_date",
  "base_value",
  "total_number_of_constituents",
  "exchange_performance_metric_id",
  "ranking_method_code",
  "weighting_method_code",
  "rebalancing_schedule",
  "computation_method",
  "created_at",
  "created_by",
  "updated_at",
  "updated_by"
) VALUES
  (1, 'TOP100', 'Top 100 Index', 'An index of equally weighted top 100 stocks by market capitalization.', '2024-01-01', 1000.0000, 100, 1, 'MARKET_CAP', 'EQUAL', '**-**-****', 'stored_procedure.build_top100_index',NOW(), 'system', NOW(), 'system');

COMMIT;