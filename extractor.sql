CREATE DATABASE hashes;
USE hashes;
CREATE USER ''@'localhost' IDENTIFIED BY '';
GRANT SELECT, INSERT, UPDATE, DELETE ON hashes.* TO ''@'localhost';
CREATE TABLE passwords (pass varchar (512)) ENGINE = InnoDB;
