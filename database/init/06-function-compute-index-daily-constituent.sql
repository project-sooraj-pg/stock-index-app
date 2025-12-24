-- PROCEDURE: public.build_index_constituents(smallint, date, date)

-- DROP PROCEDURE IF EXISTS public.build_index_constituents(smallint, date, date);

CREATE OR REPLACE FUNCTION public.compute_index_daily_constituent(
    p_total_number_of_constituents smallint,
    p_start_date date,
    p_end_date date DEFAULT NULL::date
)
RETURNS TABLE(status text, message text)
LANGUAGE plpgsql
AS $BODY$
DECLARE
    v_end_date DATE;
    v_min_trade_date DATE;
    v_max_trade_date DATE;
    v_rows_inserted INTEGER := 0;
BEGIN
    -- Get the min and max trade_date from listing_daily_performance
    SELECT MIN(trade_date), MAX(trade_date)
      INTO v_min_trade_date, v_max_trade_date
      FROM listing_daily_performance;

    -- Check if start_date and end_date are within the available range
    IF p_start_date < v_min_trade_date OR (p_end_date IS NOT NULL AND p_end_date > v_max_trade_date) THEN
        RETURN QUERY SELECT 'FAILED', 'start_date and end_date should be within ' || v_min_trade_date || ' and ' || v_max_trade_date;
        RETURN;
    END IF;

    -- Truncate the table to ensure idempotency
    TRUNCATE TABLE index_daily_constituent;

    -- Determine end date if not provided
    IF p_end_date IS NULL THEN
        SELECT MAX(trade_date) INTO v_end_date FROM view_listing_daily_market_cap_with_rank;
    ELSE
        v_end_date := p_end_date;
    END IF;

    -- Insert new constituents
    BEGIN
        INSERT INTO index_daily_constituent (
            trade_date,
            listing_id,
            market_cap_rank,
            created_at,
            created_by
        )
        SELECT
            trade_date,
            listing_id,
            market_cap_rank,
            NOW(),
            'system'
        FROM view_listing_daily_market_cap_with_rank
        WHERE trade_date BETWEEN p_start_date AND v_end_date
          AND market_cap_rank < p_total_number_of_constituents + 1;
        GET DIAGNOSTICS v_rows_inserted = ROW_COUNT;
        RETURN QUERY SELECT 'SUCCESS', v_rows_inserted::text;
    EXCEPTION WHEN OTHERS THEN
        RETURN QUERY SELECT 'FAILED', 'Error inserting index_daily_constituent: ' || SQLERRM;
    END;
END;
$BODY$;
ALTER FUNCTION public.compute_index_daily_constituent(smallint, date, date)
    OWNER TO "db-owner";