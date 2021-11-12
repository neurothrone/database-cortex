USE `py-db`;

CREATE TABLE IF NOT EXISTS users
(
    id_users  INTEGER PRIMARY KEY AUTO_INCREMENT,
    username  VARCHAR(45) NOT NULL UNIQUE,
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username)
VALUES ('zane'),
       ('ahmed'),
       ('danny'),
       ('jonas');

SELECT *
FROM users;


CREATE TABLE IF NOT EXISTS persons
(
    id_persons INTEGER PRIMARY KEY AUTO_INCREMENT,
    name       VARCHAR(100) NOT NULL,
    surname    VARCHAR(100) NOT NULL
);

INSERT INTO persons (name, surname)
VALUES ('zaid', 'neurothrone'),
       ('ahmed', 'jaborie'),
       ('daniel', 'lovened'),
       ('jonas', 'dahlqvist');

SELECT *
FROM persons;

CREATE TABLE IF NOT EXISTS cars
(
    id_cars  INTEGER PRIMARY KEY AUTO_INCREMENT,
    reg_no   VARCHAR(7) NOT NULL UNIQUE,
    model    VARCHAR(50),
    id_owner INTEGER,
    -- CONSTRAINT fk_person
    FOREIGN KEY (id_owner) REFERENCES persons (id_persons)
);

INSERT INTO cars (reg_no, model, id_owner)
VALUES ('ABC 123', 'Volvo', 3),
       ('DEF 345', 'Saab', 4),
       ('GHI 456', 'Volkswagen', 4),
       ('JKL 998', 'Opel', 1),
       ('MNO 343', 'Volvo', 1),
       ('PQR 333', 'Audi', 2),
       ('STU 664', 'Fiat', 2),
       ('VWX 444', 'DKW', 1);

SELECT *
FROM cars;

SELECT p.name, p.surname, c.reg_no, c.model
FROM persons p
         JOIN cars c ON p.id_persons = c.id_owner;
-- WHERE p.id_persons = c.id_owner;

-- admin user has no rights
# CREATE DATABASE `py-db2`;
