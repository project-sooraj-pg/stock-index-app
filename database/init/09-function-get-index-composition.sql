-- FUNCTION: public.get_index_composition(date)

-- DROP FUNCTION IF EXISTS public.get_index_composition(date);

CREATE OR REPLACE FUNCTION public.get_index_composition(
	p_trade_date date)
    RETURNS TABLE(trade_date date, company_name character varying, ticker_symbol character varying, market_cap_rank smallint)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
    v_min_date DATE;
    v_max_date DATE;
BEGIN
    -- 1. Basic validation
    IF p_trade_date IS NULL THEN
        RAISE EXCEPTION
            'trade_date cannot be NULL'
            USING ERRCODE = '22004'; -- null_value_not_allowed
    END IF;

    -- 2. Available data range
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

    -- 3. Range validation
    IF p_trade_date < v_min_date OR p_trade_date > v_max_date THEN
        RAISE EXCEPTION
            'Requested trade_date (%) is outside available data range (%)–(%)',
            p_trade_date, v_min_date, v_max_date
            USING ERRCODE = '22023'; -- invalid_parameter_value
    END IF;

    -- 4. Existence check
    IF NOT EXISTS (
        SELECT 1
        FROM index_daily_constituent idc
        WHERE idc.trade_date = p_trade_date
    ) THEN
        RAISE EXCEPTION
            'No index composition available for trade_date (%)',
            p_trade_date
            USING ERRCODE = '22023';
    END IF;

    -- 5. Return index composition
    RETURN QUERY
    SELECT
        idc.trade_date,
        c.company_name,
        l.ticker_symbol,
        idc.market_cap_rank
    FROM index_daily_constituent idc
    JOIN listing l
        ON l.listing_id = idc.listing_id
    JOIN company c
        ON c.company_id = l.company_id
    WHERE idc.trade_date = p_trade_date
    ORDER BY idc.market_cap_rank;
END;
$BODY$;

ALTER FUNCTION public.get_index_composition(date)
    OWNER TO "db-owner";

