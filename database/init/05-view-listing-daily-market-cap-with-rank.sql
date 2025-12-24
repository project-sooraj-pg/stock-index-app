-- View: public.listing_trade_date_market_cap_rank

-- DROP VIEW public.listing_trade_date_market_cap_rank;

CREATE OR REPLACE VIEW public.view_listing_daily_market_cap_with_rank
 AS
 SELECT
    ldp.listing_id,
    ldp.trade_date,
    lmc.market_cap,
    rank() OVER (PARTITION BY ldp.trade_date ORDER BY lmc.market_cap DESC) AS market_cap_rank
   FROM listing_daily_performance ldp
     LEFT JOIN LATERAL ( SELECT lmc_1.market_cap
           FROM listing_market_cap_change lmc_1
          WHERE lmc_1.listing_id = ldp.listing_id AND lmc_1.change_date <= ldp.trade_date
          ORDER BY lmc_1.change_date DESC
         LIMIT 1) lmc ON true
  WHERE lmc.market_cap IS NOT NULL;

ALTER TABLE public.view_listing_daily_market_cap_with_rank
    OWNER TO "db-owner";