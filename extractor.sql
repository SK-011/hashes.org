CREATE DATABASE hashes;
USE hashes;
CREATE USER 'hashes'@'localhost' IDENTIFIED BY 'h@5h35';
GRANT SELECT, INSERT, UPDATE, DELETE ON hashes.* TO 'hashes'@'localhost';
CREATE TABLE passwords (pass varchar (512)) ENGINE = InnoDB;



# CREATE TABLE passwords (pass varchar (512) PRIMARY KEY) ENGINE = InnoDB;
