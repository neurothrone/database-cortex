-- general form
-- SELECT AGG_FUNCTION(column_name) from table_name;
-- AGG_FUNCTIONS
--  MIN
--  MAX
--  AVG
--  COUNT
--  SUM

-- COUNT()
--  COUNT(column_name): num of rows - null values
--  COUNT(*): number of rows
--  COUNT(DISTINCT column_name): unique not null values
-- NOTE: All aggregate functions except COUNT(*) ignore the NULL values.

-- one approach
/*
SELECT
  MAX(current_location)
FROM
  agents
;
*/
-- another
SELECT
  current_location
FROM
  agents
ORDER BY
  current_location
DESC LIMIT 1
;


SELECT
  MIN(length) AS minimum,
  AVG(length) AS average,
  MAX(length) AS maximum
FROM
  streets
;

SELECT
  AVG(users_rating) AS "average user rating",
  AVG(critics_rating) AS "average critic rating"
FROM
  games
WHERE
  users_rating >= 8 AND critics_rating >= 8
;
