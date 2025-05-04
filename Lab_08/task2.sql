EXPLAIN ANALYZE
SELECT * 
FROM Ticket_flights 
WHERE ticket_no LIKE '00054343%';
--Excution Time: 190.280 ms

CREATE INDEX ticket_no_index 
ON Ticket_flights(ticket_no);

EXPLAIN ANALYZE
SELECT * 
FROM Ticket_flights 
WHERE ticket_no LIKE '00054343%';
--Excution Time: 181.799 ms
