-- IN sql you comment using the two dashes
-- This is the schema.sql file which will contain the database schema for our application   
-- the first step we took was creating our database
create database flaskproject;

-- the second step we need to take is using this database
use flaskproject;

-- the third step is creating our user table
create table if not exists users(
   id int auto_increment primary key, 
   username varchar(50) not null unique,
   email varchar(100) not null unique,
   password varchar(255) not null unique,
   balance decimal(10,2) default 50.00, --preloaded balance
   is_verified boolean default false,
   created_at timestamp default current_timestamp
);

CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    email VARCHAR(255),
    comment TEXT NOT NULL
);