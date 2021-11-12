USE db1;

INSERT INTO users(username, joined_at)
VALUES ('zane', CURRENT_TIMESTAMP),
       ('ahmed', CURRENT_TIMESTAMP),
       ('danny', CURRENT_TIMESTAMP),
       ('jonas', CURRENT_TIMESTAMP);
-- date format: YYYY MM DD HH:MM:SS

SELECT *
FROM users;

INSERT INTO courses(name, description)
VALUES ('fundamental python programming', 'yep'),
       ('database technologies', 'mashala'),
       ('web frameworks', 'woooh');

SELECT *
FROM courses;

INSERT INTO users_has_courses (users_id_users, courses_id_courses)
VALUES (1, 1),
       (2, 1),
       (3, 1),
       (4, 1),
       (2, 2),
       (4, 2);

-- get username and course name from all users that go a specific course
SELECT u.username, c.name
FROM users u
         JOIN users_has_courses uhc
              ON u.id_users = uhc.users_id_users
         JOIN courses c
              ON c.id_courses = uhc.courses_id_courses
WHERE c.id_courses = 2;
