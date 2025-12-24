-- FUNCTION: public.get_index_performance(date, date)

-- DROP FUNCTION IF EXISTS public.get_index_performance(date, date);

CREATE OR REPLACE FUNCTION public.get_index_performance(
	p_start_date date,
	p_end_date date)
    RETURNS TABLE(trade_date date, index_value double precision, daily_return_in_percentage double precision, cumulative_return_in_percentage double precision)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
    v_min_date DATE;
    v_max_date DATE;
BEGIN
    -- 1. Sanity check
    IF p_start_date > p_end_date THEN
        RAISE EXCEPTION
            'Invalid date range: start_date (%) is after end_date (%)',
            p_start_date, p_end_date
            USING ERRCODE = '22023';
    END IF;

    -- 2. Available data range
    SELECT
        MIN(idp.trade_date),
        MAX(idp.trade_date)
    INTO
        v_min_date,
        v_max_date
    FROM index_daily_performance idp;

    IF v_min_date IS NULL THEN
        RAISE EXCEPTION
            'Index data is empty'
            USING ERRCODE = 'P0001';
    END IF;

    -- 3. Strict boundary enforcement
    IF p_start_date < v_min_date OR p_end_date > v_max_date THEN
        RAISE EXCEPTION
            'Requested range (%)–(%) is outside available data range (%)–(%)',
            p_start_date, p_end_date,
            v_min_date, v_max_date
            USING ERRCODE = '22023';
    END IF;

    -- 4. Return performance data
    RETURN QUERY
    WITH ordered_data AS (
        SELECT
            idp.trade_date,
            idp.index_value::DOUBLE PRECISION AS index_value,
            LAG(idp.index_value) OVER (ORDER BY idp.trade_date) AS prev_index_value,
            FIRST_VALUE(idp.index_value) OVER (ORDER BY idp.trade_date) AS base_index_value
        FROM index_daily_performance idp
        WHERE idp.trade_date BETWEEN p_start_date AND p_end_date
    )
    SELECT
        od.trade_date,
        od.index_value,
        CASE
            WHEN od.prev_index_value IS NULL THEN 0.0
            ELSE ((od.index_value / od.prev_index_value) - 1) * 100
        END AS daily_return_in_percentage,
        ((od.index_value / od.base_index_value) - 1) * 100
            AS cumulative_return_in_percentage
    FROM ordered_data od
    ORDER BY od.trade_date;
END;
$BODY$;

ALTER FUNCTION public.get_index_performance(date, date)
    OWNER TO "db-owner";

