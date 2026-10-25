CREATE DATABASE IF NOT EXISTS salesanalytics;

USE salesanalytics;

SHOW TABLES;

SELECT COUNT(*) AS total_bookings
FROM salesanalytics.ncr_ride_bookings;
DESCRIBE salesanalytics.ncr_ride_bookings;
SELECT *
FROM salesanalytics.ncr_ride_bookings
LIMIT 10;