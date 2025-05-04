CREATE OR REPLACE FUNCTION get_valid_coordinates()
RETURNS TABLE (airport_code TEXT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION)
LANGUAGE SQL AS $$
SELECT airport_code, (coordinates[0]) AS latitude, (coordinates[1]) AS longitude
FROM airports_data
WHERE coordinates[0] BETWEEN 35 AND 50 
AND coordinates[1] BETWEEN 35 AND 50;
$$;

--After running the python script
SELECT * FROM Address;