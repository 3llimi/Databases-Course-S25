EXPLAIN ANALYZE
SELECT t.passenger_name, t.book_ref, t.ticket_no, b.book_date
FROM tickets t
JOIN bookings b ON t.book_ref = b.book_ref
WHERE t.book_ref LIKE 'B%' 
AND t.ticket_no LIKE '000543%';
--Excution Time: 215.759 ms
CREATE INDEX book_ref_idx ON bookings(book_ref);

EXPLAIN ANALYZE
SELECT t.passenger_name, t.book_ref, t.ticket_no, b.book_date
FROM tickets t
JOIN bookings b ON t.book_ref = b.book_ref
WHERE t.book_ref LIKE 'B%' 
AND t.ticket_no LIKE '000543%';
--Excution Time: 202.292 ms

CREATE INDEX book_ref_book_date_idx ON bookings(book_ref, book_date);

EXPLAIN ANALYZE
SELECT t.passenger_name, t.book_ref, t.ticket_no, b.book_date
FROM tickets t
JOIN bookings b ON t.book_ref = b.book_ref
WHERE t.book_ref LIKE 'B%' 
AND t.ticket_no LIKE '000543%';
--Excution Time: 193.703 ms
