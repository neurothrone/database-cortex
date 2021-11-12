USE db1;

CREATE TABLE IF NOT EXISTS users
(
    id_users  INT PRIMARY KEY AUTO_INCREMENT,
    username  VARCHAR(45) NOT NULL UNIQUE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses
(
    id_courses  INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    description TEXT
);

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
       ('fundamental python programming', 'woooh');

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