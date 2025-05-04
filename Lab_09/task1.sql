CREATE OR REPLACE FUNCTION retrieveFlights(start INT, "end" INT)
RETURNS TABLE(
    flight_id INT, 
    flight_no CHAR(6),
    scheduled_departure TIMESTAMPTZ,
    scheduled_arrival TIMESTAMPTZ
) AS $$
BEGIN
    IF start < 0 OR "end" < 0 THEN
        RAISE EXCEPTION 'Start and end parameters must be non-negative.';
    END IF;

    IF start > "end" THEN
        RAISE EXCEPTION 'Start parameter must be less than or equal to end parameter.';
    END IF;

    RETURN QUERY
    SELECT Flights.flight_id, Flights.flight_no, Flights.scheduled_departure, Flights.scheduled_arrival
    FROM Flights
    ORDER BY Flights.flight_id
    OFFSET start - 1 LIMIT "end" - start + 1;
END;
$$ LANGUAGE plpgsql;


SELECT * FROM retrieveFlights(10, 60);