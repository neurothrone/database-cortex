CREATE TABLE IF NOT EXISTS users
(
    id_users INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(45) NOT NULL UNIQUE,
    name     VARCHAR(100),
    surname  VARCHAR(100)
);

INSERT INTO users(username, name, surname)
VALUES ('zane', 'zaid', 'neurothrone');

SELECT *
FROM users;

INSERT INTO users(username, name, surname)
VALUES ('zane', 'zane', 'neurothrone')
ON CONFLICT DO NOTHING;


SELECT *
FROM users;

UPDATE users SET name = 'zane' WHERE LOCATE('zane', username) > 0;

SELECT *
FROM users;

-- DROP TABLE users;