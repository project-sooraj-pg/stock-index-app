-- PROCEDURE: public.compute_index_daily_performance(numeric)

-- DROP PROCEDURE IF EXISTS public.compute_index_daily_performance(numeric);

CREATE OR REPLACE PROCEDURE public.compute_index_daily_performance(
	IN p_base_value numeric DEFAULT NULL::numeric)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    v_base_date   DATE;
    v_base_value  NUMERIC;
BEGIN

    -- Truncate the table to ensure idempotency
    TRUNCATE TABLE index_daily_performance;

    -- 1. determine base date
    SELECT MIN(trade_date)
    INTO v_base_date
    FROM index_daily_constituent;

    IF v_base_date IS NULL THEN
        RAISE EXCEPTION 'No constituents found for building index performance';
    END IF;

    -- 2. determine base value - sum of close_price of index constituents
    IF p_base_value IS NOT NULL THEN
        v_base_value := p_base_value;
    ELSE
        SELECT SUM(ldp.close_price)
        INTO v_base_value
        FROM index_daily_constituent idc
        JOIN listing_daily_performance ldp
          ON ldp.listing_id = idc.listing_id
         AND ldp.trade_date = idc.trade_date
        WHERE idc.trade_date = v_base_date;

        IF v_base_value IS NULL THEN
            RAISE EXCEPTION 'unable to compute base value';
        END IF;
    END IF;

    -- 3. insert base day index value
    INSERT INTO index_daily_performance (trade_date, index_value, created_at, created_by)
    VALUES (v_base_date, v_base_value, NOW(), 'system')
    ON CONFLICT (trade_date) DO NOTHING;

    -- 4. compute and insert subsequent index values
    INSERT INTO index_daily_performance (trade_date, index_value, created_at, created_by)
    SELECT
        --- trade date
        d.trade_date AS trade_date,
        --- index value as base value * cumulative product of price ratio
        v_base_value
        * EXP(SUM(LN(d.avg_price_ratio))
              OVER (ORDER BY d.trade_date
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)) AS index_value,
        NOW() AS created_at,
        'system' AS created_by
    FROM (
        SELECT
            --- trade date
            trade_date,
            --- average price ratio of index constituent on that date
            AVG(price_ratio) AS avg_price_ratio
        FROM (
            SELECT
                -- trade date
                idc.trade_date,
                -- listing_id
                idc.listing_id,
                -- price_ratio: price ratio of listing_id on trade date
                -- (close_price/previous_close)
                ldp.close_price
                / LAG(ldp.close_price) OVER (
                    PARTITION BY idc.listing_id
                    ORDER BY idc.trade_date
                ) AS price_ratio
            FROM index_daily_constituent idc
            JOIN listing_daily_performance ldp
              ON ldp.listing_id = idc.listing_id
             AND ldp.trade_date = idc.trade_date
            -- IMPORTANT:
            -- DO NOT filter by base_date here.
            -- LAG() must see the base_date row so that
            -- the first computed day has a valid ratio.
        ) t --- price ratio computation
        WHERE price_ratio IS NOT NULL
          AND trade_date > v_base_date   -- <-- filter AFTER ratio computation
        GROUP BY trade_date
    ) d ---average price ratio computation
    ORDER BY d.trade_date;

END;
$BODY$;
ALTER PROCEDURE public.compute_index_daily_performance(numeric)
    OWNER TO "db-owner";