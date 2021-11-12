SELECT col_name
FROM table_name
WHERE expression
GROUP BY col_name;

SELECT
  tutor_name,
  MIN(capacity)
FROM
  tutors
GROUP BY
  tutor_name
HAVING
  MIN(capacity) > 30
;

SELECT
  release_year,
  AVG(budget) AS "average budget",
  AVG(box_office) AS "average box office"
FROM
  movies
GROUP BY
  release_year
;
