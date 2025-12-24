-- FUNCTION: public.get_index_composition_change(date, date)

-- DROP FUNCTION IF EXISTS public.get_index_composition_change(date, date);

CREATE OR REPLACE FUNCTION public.get_index_composition_change(
	p_start_date date,
	p_end_date date)
    RETURNS TABLE(change_date date, company_name character varying, ticker_symbol character varying, action character varying)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
    v_min_date DATE;
    v_max_date DATE;
    v_start_date DATE;
    v_end_date DATE;
BEGIN
    -- 1. Available data range
    SELECT
        MIN(idc.trade_date),
        MAX(idc.trade_date)
    INTO
        v_min_date,
        v_max_date
    FROM index_daily_constituent idc;

    IF v_min_date IS NULL THEN
        RAISE EXCEPTION
            'Index composition data is empty'
            USING ERRCODE = 'P0001';
    END IF;

    -- 2. Use min/max if input is null
    v_start_date := COALESCE(p_start_date, v_min_date);
    v_end_date := COALESCE(p_end_date, v_max_date);

    -- 3. Sanity check
    IF v_start_date > v_end_date THEN
        RAISE EXCEPTION
            'Invalid date range: start_date (%) is after end_date (%)',
            v_start_date, v_end_date
            USING ERRCODE = '22023';
    END IF;

    -- 4. Strict boundary enforcement
    IF v_start_date < v_min_date OR v_end_date > v_max_date THEN
        RAISE EXCEPTION
            'Requested range (%)–(%) is outside available data range (%)–(%)',
            v_start_date, v_end_date,
            v_min_date, v_max_date
            USING ERRCODE = '22023';
    END IF;

    -- 5. Return constituent changes
    RETURN QUERY
    WITH ordered_dates AS (
        SELECT DISTINCT trade_date
        FROM index_daily_constituent
        WHERE trade_date BETWEEN v_start_date AND v_end_date
        ORDER BY trade_date
    ),
    date_pairs AS (
        SELECT
            trade_date AS current_date,
            LAG(trade_date) OVER (ORDER BY trade_date) AS previous_date
        FROM ordered_dates
    ),

    -- Added constituents
    added AS (
        SELECT
            dp.current_date AS change_date,
            idc.listing_id
        FROM date_pairs dp
        JOIN index_daily_constituent idc
            ON idc.trade_date = dp.current_date
        LEFT JOIN index_daily_constituent prev
            ON prev.trade_date = dp.previous_date
           AND prev.listing_id = idc.listing_id
        WHERE dp.previous_date IS NOT NULL
          AND prev.listing_id IS NULL
    ),

    -- Removed constituents
    removed AS (
        SELECT
            dp.current_date AS change_date,
            prev.listing_id
        FROM date_pairs dp
        JOIN index_daily_constituent prev
            ON prev.trade_date = dp.previous_date
        LEFT JOIN index_daily_constituent idc
            ON idc.trade_date = dp.current_date
           AND idc.listing_id = prev.listing_id
        WHERE dp.previous_date IS NOT NULL
          AND idc.listing_id IS NULL
    )

    SELECT
        a.change_date,
        c.company_name,
        l.ticker_symbol,
        'Added'::VARCHAR AS action
    FROM added a
    JOIN listing l
        ON l.listing_id = a.listing_id
    JOIN company c
        ON c.company_id = l.company_id

    UNION ALL

    SELECT
        r.change_date,
        c.company_name,
        l.ticker_symbol,
        'Removed'::VARCHAR AS action
    FROM removed r
    JOIN listing l
        ON l.listing_id = r.listing_id
    JOIN company c
        ON c.company_id = l.company_id

    ORDER BY change_date, action, ticker_symbol;
END;
$BODY$;

ALTER FUNCTION public.get_index_composition_change(date, date)
    OWNER TO "db-owner";

