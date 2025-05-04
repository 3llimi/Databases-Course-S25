SELECT DISTINCT f.flight_no
FROM Flights f
JOIN Ticket_flights tf ON f.flight_id = tf.flight_id
JOIN Tickets t ON tf.ticket_no = t.ticket_no
WHERE t.passenger_name LIKE 'M%';

CREATE INDEX passenger_name_idx 
ON Tickets(passenger_name);

CREATE INDEX ticket_no_idx 
ON Ticket_flights(ticket_no);

CREATE INDEX flight_id_idx 
ON Ticket_flights(flight_id);

EXPLAIN ANALYZE
SELECT f.flight_no
FROM Flights f
WHERE EXISTS (
    SELECT 1
    FROM Ticket_flights tf
    JOIN Tickets t ON tf.ticket_no = t.ticket_no
    WHERE f.flight_id = tf.flight_id 
    AND t.passenger_name LIKE 'M%'
);
--Excution Time: 363.670 ms
