USE db1;

CREATE TABLE IF NOT EXISTS users
(
    id_users  INT PRIMARY KEY AUTO_INCREMENT,
    username  VARCHAR(100) NOT NULL UNIQUE,
    name      VARCHAR(100),
    surname   VARCHAR(100),
    age       INT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users(username, name, surname, age)
VALUES ('zane', 'Zaid', 'Neurothrone', 30);

SELECT *
FROM users;

SELECT username, joined_at
FROM users;

SELECT *
FROM users
WHERE username = 'zane';

INSERT INTO users(username, name, surname, age)
VALUES ('danzel', 'Danny', 'Feedington', 30),
       ('sanoj', 'Jonas', 'Dahlqvist', 34),
       ('ahmed', 'Ahmed', 'Jaborie', 59);

SELECT *
FROM users;

SELECT *
FROM users
ORDER BY username;

SELECT CONCAT(name, ' ', surname) AS full_name
FROM users
ORDER BY name;

SELECT *
FROM users
WHERE age < 40;

-- % wildcard: %ton ends with ton. Z% starts with Z
SELECT *
FROM users
WHERE surname LIKE '%ton';

SELECT *
FROM users
WHERE surname like '%on%';

DROP TABLE IF EXISTS users;

UPDATE users
SET username = 'danny'
WHERE username = 'danzel';

SELECT *
FROM users;