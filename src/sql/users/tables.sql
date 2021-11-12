CREATE TABLE IF NOT EXISTS users
(
    id_users INTEGER      NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    joined   DATETIME
);

CREATE TABLE IF NOT EXISTS courses
(
    id_courses  INTEGER     NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(45) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS course_sections
(
    id_course_sections INTEGER     NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name               VARCHAR(45) NOT NULL
        CONSTRAINT fk_courses FOREIGN KEY
            REFERENCES courses (id_courses)
);

CREATE TABLE IF NOT EXISTS course_modules
(
    id_course_modules INTEGER     NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name              VARCHAR(45) NOT NULL,
    content           TEXT        NOT NULL
        CONSTRAINT fk_course_sections FOREIGN KEY
            REFERENCES course_sections (id_course_sections)
);
