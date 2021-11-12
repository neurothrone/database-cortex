CREATE TABLE IF NOT EXISTS users
(
    id_users INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(45) NOT NULL UNIQUE,
    name     VARCHAR(100),
    surname  VARCHAR(100)
);

INSERT INTO users(username, name, surname)
VALUES ('zane', 'zaid', 'neurothrone'),
       ('ahmed', 'ahmad', 'jaborie');

SELECT *
FROM users;

-- deletes everything from the table
DELETE FROM users;

DELETE FROM users
WHERE username = 'zane';

DROP TABLE users;
