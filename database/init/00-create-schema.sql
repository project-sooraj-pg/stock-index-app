BEGIN;

CREATE TABLE "country" (
  "country_code" varchar(4) PRIMARY KEY,
  "country_name" varchar(64),
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "company" (
  "company_id" integer PRIMARY KEY,
  "company_name" varchar(128) NOT NULL,
  "company_description" varchar(1024),
  "country_code" varchar(8) NOT NULL,
  "website" varchar(128),
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "exchange" (
  "exchange_id" integer PRIMARY KEY,
  "exchange_code" varchar(8) NOT NULL,
  "exchange_name" varchar(128) NOT NULL,
  "exchange_description" varchar(1024),
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "listing_status" (
  "listing_status_code" varchar(4) PRIMARY KEY,
  "listing_status" varchar(8) NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "listing_type" (
  "listing_type_code" varchar(8) PRIMARY KEY,
  "listing_type_name" varchar(64) NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "listing" (
  "listing_id" integer PRIMARY KEY,
  "company_id" integer NOT NULL,
  "exchange_id" integer NOT NULL,
  "ticker_symbol" varchar(8) NOT NULL,
  "listing_type_code" varchar(8),
  "listing_status_code" varchar(4) NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "listing_daily_performance" (
  "listing_id" integer NOT NULL,
  "trade_date" date NOT NULL,
  "open_price" numeric(12,4),
  "high_price" numeric(12,4),
  "low_price" numeric(12,4),
  "close_price" numeric(12,4),
  "trade_volume" bigint,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64),
  CONSTRAINT "enforce_non_negative_open_price" CHECK (open_price >= 0),
  CONSTRAINT "enforce_non_negative_high_price" CHECK (high_price >= 0),
  CONSTRAINT "enforce_non_negative_low_price" CHECK (low_price >= 0),
  CONSTRAINT "enforce_non_negative_close_price" CHECK (close_price >= 0),
  CONSTRAINT "enforce_high_price_not_less_than_low_price" CHECK (high_price >= low_price),
  CONSTRAINT "enforce_valid_open_price" CHECK (open_price BETWEEN low_price AND high_price),
  CONSTRAINT "enforce_valid_close_price" CHECK (close_price BETWEEN low_price AND high_price),
  CONSTRAINT "enforce_non_negative_trade_volume" CHECK (trade_volume >= 0),
  PRIMARY KEY ("listing_id", "trade_date")
);

CREATE TABLE "listing_market_cap_change" (
  "listing_id" integer NOT NULL,
  "change_date" date NOT NULL,
  "market_cap" numeric(20,4),
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64),
  PRIMARY KEY ("listing_id", "change_date")
);

CREATE TABLE "ranking_method" (
  "ranking_method_code" varchar(16) PRIMARY KEY,
  "ranking_method_description" varchar(1024) NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "weighting_method" (
  "weighting_method_code" varchar(16) PRIMARY KEY,
  "weighting_method_description" varchar(1024) NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "performance_metric" (
  "performance_metric_id" smallint PRIMARY KEY,
  "performance_metric_name" varchar(16) NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "exchange_performance_metric" (
  "exchange_performance_metric_id" integer PRIMARY KEY,
  "exchange_performance_metric_description" varchar(1024) NOT NULL,
  "performance_metric_id" smallint NOT NULL,
  "exchange_id" integer NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "index_definition" (
  "index_definition_id" integer PRIMARY KEY,
  "index_code" varchar(16) NOT NULL,
  "index_name" varchar(128) NOT NULL,
  "index_description" varchar(1024),
  "base_date" date NOT NULL,
  "base_value" numeric(12,4) NOT NULL,
  "total_number_of_constituents" smallint NOT NULL,
  "exchange_performance_metric_id" integer NOT NULL,
  "ranking_method_code" varchar(16) NOT NULL,
  "weighting_method_code" varchar(16) NOT NULL,
  "rebalancing_schedule" varchar(16) NOT NULL,
  "computation_method" varchar(64) NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64),
  CONSTRAINT "enforce_positive_total_number_of_constituents" CHECK (total_number_of_constituents > 0),
  CONSTRAINT "enforce_positive_base_value" CHECK (base_value > 0)
);

CREATE TABLE "index_constituent_base" (
  "index_definition_id" integer NOT NULL,
  "listing_id" integer NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64),
  PRIMARY KEY ("index_definition_id", "listing_id")
);

CREATE TABLE "index_daily_performance" (
  "index_definition_id" integer NOT NULL,
  "trade_date" date NOT NULL,
  "index_value" numeric(12,4) NOT NULL,
  "daily_return" numeric(12,4),
  "cumulative_return" numeric(12,4),
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64),
  PRIMARY KEY ("index_definition_id", "trade_date")
);

CREATE TABLE "index_rebalance" (
  "index_rebalance_id" integer PRIMARY KEY,
  "index_definition_id" integer NOT NULL,
  "rebalance_date" date NOT NULL,
  "adjusted_divisor" numeric(12,4) NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "constituent_change_type" (
  "constituent_change_type_code" varchar(8) PRIMARY KEY,
  "constituent_change_type_description" varchar(1024) NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE TABLE "index_constituent_change" (
  "index_rebalance_id" integer NOT NULL,
  "listing_id" integer NOT NULL,
  "constituent_change_type_code" varchar(8),
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64),
  PRIMARY KEY ("index_rebalance_id", "listing_id")
);

CREATE INDEX ON "listing" ("company_id");

CREATE UNIQUE INDEX ON "listing" ("ticker_symbol", "exchange_id");

CREATE UNIQUE INDEX ON "index_definition" ("index_code");

CREATE UNIQUE INDEX ON "index_rebalance" ("index_definition_id", "rebalance_date");

ALTER TABLE "company" ADD FOREIGN KEY ("country_code") REFERENCES "country" ("country_code");

ALTER TABLE "listing" ADD FOREIGN KEY ("listing_status_code") REFERENCES "listing_status" ("listing_status_code");

ALTER TABLE "listing" ADD FOREIGN KEY ("listing_type_code") REFERENCES "listing_type" ("listing_type_code");

ALTER TABLE "listing" ADD FOREIGN KEY ("company_id") REFERENCES "company" ("company_id");

ALTER TABLE "listing" ADD FOREIGN KEY ("exchange_id") REFERENCES "exchange" ("exchange_id");

ALTER TABLE "listing_market_cap_change" ADD FOREIGN KEY ("listing_id") REFERENCES "listing" ("listing_id");

ALTER TABLE "exchange_performance_metric" ADD FOREIGN KEY ("performance_metric_id") REFERENCES "performance_metric" ("performance_metric_id");

ALTER TABLE "exchange_performance_metric" ADD FOREIGN KEY ("exchange_id") REFERENCES "exchange" ("exchange_id");

ALTER TABLE "index_definition" ADD FOREIGN KEY ("ranking_method_code") REFERENCES "ranking_method" ("ranking_method_code");

ALTER TABLE "index_definition" ADD FOREIGN KEY ("weighting_method_code") REFERENCES "weighting_method" ("weighting_method_code");

ALTER TABLE "index_definition" ADD FOREIGN KEY ("exchange_performance_metric_id") REFERENCES "exchange_performance_metric" ("exchange_performance_metric_id");

ALTER TABLE "index_constituent_base" ADD FOREIGN KEY ("listing_id") REFERENCES "listing" ("listing_id");

ALTER TABLE "index_constituent_base" ADD FOREIGN KEY ("index_definition_id") REFERENCES "index_definition" ("index_definition_id");

ALTER TABLE "index_daily_performance" ADD FOREIGN KEY ("index_definition_id") REFERENCES "index_definition" ("index_definition_id");

ALTER TABLE "index_rebalance" ADD FOREIGN KEY ("index_definition_id") REFERENCES "index_definition" ("index_definition_id");

ALTER TABLE "index_constituent_change" ADD FOREIGN KEY ("constituent_change_type_code") REFERENCES "constituent_change_type" ("constituent_change_type_code");

ALTER TABLE "index_constituent_change" ADD FOREIGN KEY ("index_rebalance_id") REFERENCES "index_rebalance" ("index_rebalance_id");

ALTER TABLE "index_constituent_change" ADD FOREIGN KEY ("listing_id") REFERENCES "listing" ("listing_id");

COMMIT;