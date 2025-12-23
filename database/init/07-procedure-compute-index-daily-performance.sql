-- FUNCTION: public.compute_index_daily_performance(numeric)

-- DROP FUNCTION IF EXISTS public.compute_index_daily_performance(numeric);

CREATE OR REPLACE FUNCTION public.compute_index_daily_performance(
    p_base_value numeric DEFAULT NULL::numeric
)
RETURNS TABLE(status text, message text)
LANGUAGE plpgsql
AS $BODY$
DECLARE
    v_base_date   DATE;
    v_base_value  NUMERIC;
    v_rows_inserted INTEGER := 0;
    v_rows_this_insert INTEGER := 0;
BEGIN
    -- Truncate the table to ensure idempotency
    TRUNCATE TABLE index_daily_performance;

    -- 1. determine base date
    SELECT MIN(trade_date)
    INTO v_base_date
    FROM index_daily_constituent;

    IF v_base_date IS NULL THEN
        RETURN QUERY SELECT 'FAILED', 'No constituents found for building index performance';
        RETURN;
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
            RETURN QUERY SELECT 'FAILED', 'unable to compute base value';
            RETURN;
        END IF;
    END IF;

    -- 3. insert base day index value
    BEGIN
        INSERT INTO index_daily_performance (trade_date, index_value, created_at, created_by)
        VALUES (v_base_date, v_base_value, NOW(), 'system')
        ON CONFLICT (trade_date) DO NOTHING;
    EXCEPTION WHEN OTHERS THEN
        RETURN QUERY SELECT 'FAILED', 'Error inserting base day index value: ' || SQLERRM;
        RETURN;
    END;
    GET DIAGNOSTICS v_rows_this_insert = ROW_COUNT;
    v_rows_inserted := v_rows_inserted + v_rows_this_insert;

    -- 4. compute and insert subsequent index values
    BEGIN
        INSERT INTO index_daily_performance (trade_date, index_value, created_at, created_by)
        SELECT
            d.trade_date AS trade_date,
            v_base_value
            * EXP(SUM(LN(d.avg_price_ratio))
                  OVER (ORDER BY d.trade_date
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)) AS index_value,
            NOW() AS created_at,
            'system' AS created_by
        FROM (
            SELECT
                trade_date,
                AVG(price_ratio) AS avg_price_ratio
            FROM (
                SELECT
                    idc.trade_date,
                    idc.listing_id,
                    ldp.close_price
                    / LAG(ldp.close_price) OVER (
                        PARTITION BY idc.listing_id
                        ORDER BY idc.trade_date
                    ) AS price_ratio
                FROM index_daily_constituent idc
                JOIN listing_daily_performance ldp
                  ON ldp.listing_id = idc.listing_id
                 AND ldp.trade_date = idc.trade_date
            ) t
            WHERE price_ratio IS NOT NULL
              AND trade_date > v_base_date
            GROUP BY trade_date
        ) d
        ORDER BY d.trade_date;
    EXCEPTION WHEN OTHERS THEN
        RETURN QUERY SELECT 'FAILED', 'Error inserting subsequent index values: ' || SQLERRM;
        RETURN;
    END;
    GET DIAGNOSTICS v_rows_this_insert = ROW_COUNT;
    v_rows_inserted := v_rows_inserted + v_rows_this_insert;

    RETURN QUERY SELECT 'SUCCESS', v_rows_inserted::text;
END;
$BODY$;
ALTER FUNCTION public.compute_index_daily_performance(numeric)
    OWNER TO "db-owner";