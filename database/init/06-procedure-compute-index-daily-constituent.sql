-- PROCEDURE: public.build_index_constituents(smallint, date, date)

-- DROP PROCEDURE IF EXISTS public.build_index_constituents(smallint, date, date);

CREATE OR REPLACE PROCEDURE public.compute_index_daily_constituent(
	IN p_total_number_of_constituents smallint,
	IN p_start_date date,
	IN p_end_date date DEFAULT NULL::date)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    v_end_date DATE;
BEGIN
    -- Truncate the table to ensure idempotency
    TRUNCATE TABLE index_daily_constituent;

    -- Determine end date if not provided
    IF p_end_date IS NULL THEN
        SELECT MAX(trade_date) INTO v_end_date FROM view_listing_daily_market_cap_with_rank;
    ELSE
        v_end_date := p_end_date;
    END IF;

    -- Insert new constituents
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
END;
$BODY$;
ALTER PROCEDURE public.compute_index_daily_constituent(smallint, date, date)
    OWNER TO "db-owner";