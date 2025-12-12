




create database flaskproject;


use flaskproject;

-- the second step we need to take is using the database


create table if not exists users(
    id INT auto_increment primary key,
    username varchar(50) unique not null,
    email varchar(100) unique not null,
    password varchar(255) unique not null,
    phone varchar(20),
    is_vertified boolean default false,
    create_at timestamp default current_timestamp
)