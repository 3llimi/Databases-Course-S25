CREATE OR REPLACE FUNCTION retrieveFlightsPage(pageSize INT, pageNumber INT)
RETURNS TABLE(
    flight_id INT, 
    flight_no CHAR(6), 
    departure_airport CHAR(3), 
    arrival_airport CHAR(3)
) AS $$
DECLARE
    offset_value INT;
BEGIN
    IF pageSize < 0 OR pageNumber < 0 THEN
        RAISE EXCEPTION 'pageSize and pageNumber must be non-negative.';
    END IF;

    offset_value := (pageNumber - 1) * pageSize;

    RETURN QUERY
    SELECT Flights.flight_id, Flights.flight_no, Flights.departure_airport, Flights.arrival_airport
    FROM Flights
    ORDER BY Flights.flight_id
    OFFSET offset_value LIMIT pageSize;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM retrieveFlightsPage(100, 3);