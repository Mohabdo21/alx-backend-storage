-- Create a table `users` with specific attributes
-- CREATE TABLE IF NOT EXISTS users (
-- 	id INT AUTO_INCREMENT,
-- 	email VARCHAR(255) NOT NULL,
-- 	name VARCHAR(255),
-- 	PRIMARY KEY(id),
-- 	UNIQUE (email),
-- );

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    PRIMARY KEY (id),
    UNIQUE (email)
);
