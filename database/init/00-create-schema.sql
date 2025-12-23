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

CREATE TABLE "index_daily_constituent" (
  "trade_date" date NOT NULL,
  "listing_id" integer NOT NULL,
  "market_cap_rank" smallint NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64),
  PRIMARY KEY ("trade_date", "listing_id")
);

CREATE TABLE "index_daily_performance" (
  "trade_date" date PRIMARY KEY,
  "index_value" numeric(12,4) NOT NULL,
  "created_at" timestamptz,
  "created_by" varchar(64),
  "updated_at" timestamptz,
  "updated_by" varchar(64)
);

CREATE INDEX ON "listing" ("company_id");

CREATE UNIQUE INDEX ON "listing" ("ticker_symbol", "exchange_id");

ALTER TABLE "company" ADD FOREIGN KEY ("country_code") REFERENCES "country" ("country_code");

ALTER TABLE "listing" ADD FOREIGN KEY ("listing_status_code") REFERENCES "listing_status" ("listing_status_code");

ALTER TABLE "listing" ADD FOREIGN KEY ("listing_type_code") REFERENCES "listing_type" ("listing_type_code");

ALTER TABLE "listing" ADD FOREIGN KEY ("company_id") REFERENCES "company" ("company_id");

ALTER TABLE "listing" ADD FOREIGN KEY ("exchange_id") REFERENCES "exchange" ("exchange_id");

ALTER TABLE "listing_daily_performance" ADD FOREIGN KEY ("listing_id") REFERENCES "listing" ("listing_id");

ALTER TABLE "listing_market_cap_change" ADD FOREIGN KEY ("listing_id") REFERENCES "listing" ("listing_id");

ALTER TABLE "index_daily_constituent" ADD FOREIGN KEY ("listing_id") REFERENCES "listing" ("listing_id");


COMMIT;