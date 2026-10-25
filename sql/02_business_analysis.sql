
USE salesanalytics;

-- =====================================================
-- 1. OVERALL BUSINESS SUMMARY
-- =====================================================

SELECT
    COUNT(*) AS total_bookings,
    SUM(CASE
        WHEN `Booking Status` = 'Completed' THEN 1
        ELSE 0
    END) AS completed_bookings,
    SUM(CASE
        WHEN `Booking Status` LIKE 'Cancelled%' THEN 1
        ELSE 0
    END) AS cancelled_bookings,
    SUM(CASE
        WHEN `Booking Status` = 'Incomplete' THEN 1
        ELSE 0
    END) AS incomplete_bookings,
    ROUND(
        100.0 * SUM(CASE
            WHEN `Booking Status` = 'Completed' THEN 1
            ELSE 0
        END) / NULLIF(COUNT(*), 0),
        2
    ) AS completion_rate_pct
FROM ncr_ride_bookings;


-- =====================================================
-- 2. BOOKINGS BY STATUS
-- =====================================================

SELECT
    `Booking Status`,
    COUNT(*) AS total_bookings,
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*)
         FROM ncr_ride_bookings
         WHERE `Booking Status` IS NOT NULL
           AND TRIM(`Booking Status`) <> ''
           AND LOWER(TRIM(`Booking Status`)) <> 'null'),
        2
    ) AS booking_percentage
FROM ncr_ride_bookings
WHERE `Booking Status` IS NOT NULL
  AND TRIM(`Booking Status`) <> ''
  AND LOWER(TRIM(`Booking Status`)) <> 'null'
GROUP BY `Booking Status`
ORDER BY total_bookings DESC;


-- =====================================================
-- 3. BOOKINGS BY VEHICLE TYPE
-- =====================================================

SELECT
    `Vehicle Type`,
    COUNT(*) AS total_bookings,
    SUM(CASE
        WHEN `Booking Status` = 'Completed' THEN 1
        ELSE 0
    END) AS completed_bookings
FROM ncr_ride_bookings
WHERE `Vehicle Type` IS NOT NULL
  AND TRIM(`Vehicle Type`) <> ''
  AND LOWER(TRIM(`Vehicle Type`)) <> 'null'
GROUP BY `Vehicle Type`
ORDER BY total_bookings DESC;


-- =====================================================
-- 4. TOP 10 PICKUP LOCATIONS
-- =====================================================

SELECT
    `Pickup Location`,
    COUNT(*) AS total_bookings
FROM ncr_ride_bookings
WHERE `Pickup Location` IS NOT NULL
  AND TRIM(`Pickup Location`) <> ''
  AND LOWER(TRIM(`Pickup Location`)) <> 'null'
GROUP BY `Pickup Location`
ORDER BY total_bookings DESC
LIMIT 10;


-- =====================================================
-- 5. TOP 10 DROP LOCATIONS
-- =====================================================

SELECT
    `Drop Location`,
    COUNT(*) AS total_bookings
FROM ncr_ride_bookings
WHERE `Drop Location` IS NOT NULL
  AND TRIM(`Drop Location`) <> ''
  AND LOWER(TRIM(`Drop Location`)) <> 'null'
GROUP BY `Drop Location`
ORDER BY total_bookings DESC
LIMIT 10;


-- =====================================================
-- 6. BOOKINGS BY PAYMENT METHOD
-- =====================================================

SELECT
    `Payment Method`,
    COUNT(*) AS total_bookings
FROM ncr_ride_bookings
WHERE `Payment Method` IS NOT NULL
  AND TRIM(`Payment Method`) <> ''
  AND LOWER(TRIM(`Payment Method`)) <> 'null'
GROUP BY `Payment Method`
ORDER BY total_bookings DESC;


-- =====================================================
-- 7. CUSTOMER CANCELLATION REASONS
-- =====================================================

SELECT
    `Reason for cancelling by Customer` AS cancellation_reason,
    COUNT(*) AS total_cancellations
FROM ncr_ride_bookings
WHERE `Booking Status` = 'Cancelled by Customer'
  AND `Reason for cancelling by Customer` IS NOT NULL
  AND TRIM(`Reason for cancelling by Customer`) <> ''
  AND LOWER(TRIM(`Reason for cancelling by Customer`)) <> 'null'
GROUP BY `Reason for cancelling by Customer`
ORDER BY total_cancellations DESC;


-- =====================================================
-- 8. DRIVER CANCELLATION REASONS
-- =====================================================

SELECT
    `Driver Cancellation Reason` AS cancellation_reason,
    COUNT(*) AS total_cancellations
FROM ncr_ride_bookings
WHERE `Booking Status` = 'Cancelled by Driver'
  AND `Driver Cancellation Reason` IS NOT NULL
  AND TRIM(`Driver Cancellation Reason`) <> ''
  AND LOWER(TRIM(`Driver Cancellation Reason`)) <> 'null'
GROUP BY `Driver Cancellation Reason`
ORDER BY total_cancellations DESC;


-- =====================================================
-- 9. AVERAGE BOOKING VALUE FOR COMPLETED RIDES
-- =====================================================

SELECT
    COUNT(*) AS rides_with_valid_booking_value,
    ROUND(AVG(
        CAST(NULLIF(TRIM(`Booking Value`), '')
             AS DECIMAL(12,2))
    ), 2) AS average_booking_value,
    ROUND(SUM(
        CAST(NULLIF(TRIM(`Booking Value`), '')
             AS DECIMAL(12,2))
    ), 2) AS total_booking_value
FROM ncr_ride_bookings
WHERE `Booking Status` = 'Completed'
  AND `Booking Value` IS NOT NULL
  AND TRIM(`Booking Value`) <> ''
  AND LOWER(TRIM(`Booking Value`)) <> 'null'
  AND TRIM(`Booking Value`) REGEXP '^[0-9]+(\\.[0-9]+)?$';


-- =====================================================
-- 10. AVERAGE RIDE DISTANCE FOR COMPLETED RIDES
-- =====================================================

SELECT
    COUNT(*) AS rides_with_valid_distance,
    ROUND(AVG(
        CAST(NULLIF(TRIM(`Ride Distance`), '')
             AS DECIMAL(12,2))
    ), 2) AS average_ride_distance,
    ROUND(SUM(
        CAST(NULLIF(TRIM(`Ride Distance`), '')
             AS DECIMAL(12,2))
    ), 2) AS total_ride_distance
FROM ncr_ride_bookings
WHERE `Booking Status` = 'Completed'
  AND `Ride Distance` IS NOT NULL
  AND TRIM(`Ride Distance`) <> ''
  AND LOWER(TRIM(`Ride Distance`)) <> 'null'
  AND TRIM(`Ride Distance`) REGEXP '^[0-9]+(\\.[0-9]+)?$';


-- =====================================================
-- 11. CUSTOMER RATINGS
-- =====================================================

SELECT
    COUNT(*) AS rides_with_customer_rating,
    ROUND(AVG(
        CAST(NULLIF(TRIM(`Customer Rating`), '')
             AS DECIMAL(5,2))
    ), 2) AS average_customer_rating
FROM ncr_ride_bookings
WHERE `Customer Rating` IS NOT NULL
  AND TRIM(`Customer Rating`) <> ''
  AND LOWER(TRIM(`Customer Rating`)) <> 'null'
  AND TRIM(`Customer Rating`) REGEXP '^[0-9]+(\\.[0-9]+)?$';


-- =====================================================
-- 12. DRIVER RATINGS
-- =====================================================

SELECT
    COUNT(*) AS rides_with_driver_rating,
    ROUND(AVG(
        CAST(NULLIF(TRIM(`Driver Ratings`), '')
             AS DECIMAL(5,2))
    ), 2) AS average_driver_rating
FROM ncr_ride_bookings
WHERE `Driver Ratings` IS NOT NULL
  AND TRIM(`Driver Ratings`) <> ''
  AND LOWER(TRIM(`Driver Ratings`)) <> 'null'
  AND TRIM(`Driver Ratings`) REGEXP '^[0-9]+(\\.[0-9]+)?$';


-- =====================================================
-- 13. INCOMPLETE RIDE REASONS
-- =====================================================

SELECT
    `Incomplete Rides Reason` AS incomplete_reason,
    COUNT(*) AS total_incomplete_rides
FROM ncr_ride_bookings
WHERE `Booking Status` = 'Incomplete'
  AND `Incomplete Rides Reason` IS NOT NULL
  AND TRIM(`Incomplete Rides Reason`) <> ''
  AND LOWER(TRIM(`Incomplete Rides Reason`)) <> 'null'
GROUP BY `Incomplete Rides Reason`
ORDER BY total_incomplete_rides DESC;


-- =====================================================
-- 14. AVERAGE WAITING TIMES BY VEHICLE TYPE
-- =====================================================

SELECT
    `Vehicle Type`,
    COUNT(*) AS total_bookings,
    ROUND(AVG(
        CAST(NULLIF(TRIM(`Avg VTAT`), '')
             AS DECIMAL(10,2))
    ), 2) AS average_vehicle_wait_time,
    ROUND(AVG(
        CAST(NULLIF(TRIM(`Avg CTAT`), '')
             AS DECIMAL(10,2))
    ), 2) AS average_customer_wait_time
FROM ncr_ride_bookings
WHERE `Vehicle Type` IS NOT NULL
  AND TRIM(`Vehicle Type`) <> ''
  AND LOWER(TRIM(`Vehicle Type`)) <> 'null'
GROUP BY `Vehicle Type`
ORDER BY total_bookings DESC;


-- =====================================================
-- 15. COMPLETED BOOKINGS BY VEHICLE TYPE
-- =====================================================

SELECT
    `Vehicle Type`,
    COUNT(*) AS completed_bookings,
    ROUND(AVG(
        CAST(NULLIF(TRIM(`Booking Value`), '')
             AS DECIMAL(12,2))
    ), 2) AS average_booking_value,
    ROUND(AVG(
        CAST(NULLIF(TRIM(`Ride Distance`), '')
             AS DECIMAL(12,2))
    ), 2) AS average_ride_distance
FROM ncr_ride_bookings
WHERE `Booking Status` = 'Completed'
  AND `Vehicle Type` IS NOT NULL
  AND TRIM(`Vehicle Type`) <> ''
  AND LOWER(TRIM(`Vehicle Type`)) <> 'null'
GROUP BY `Vehicle Type`
ORDER BY completed_bookings DESC;
