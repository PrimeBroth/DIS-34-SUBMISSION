
drop table if exists dikumon cascade;
drop table if exists users cascade;
drop table if exists reviews cascade;

CREATE TABLE IF NOT EXISTS users(
    username char(20) NOT NULL,
    password char(20) NOT NULL,
    CONSTRAINT user_pk PRIMARY KEY (username));

create table dikumon(
number int,
name varchar(256) primary key,
type1 varchar(256),
type2 varchar(256),
total int,
hp int,
attack int,
defense int,
sp_attack int,
sp_defense int,
speed int,
generation int,
legendary boolean
);

\COPY dikumon FROM '/home/nick/MEGAsync/DIS/DIS34/DISProjekt/dikudex/tmp/Pokemon.csv' DELIMITER ',' CSV HEADER;

ALTER TABLE dikumon ADD COLUMN username char(20);
ALTER TABLE dikumon ADD FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE;

create table reviews(
    rid int primary key,
    username char(20),
    name varchar(256),
    rating int,
    review varchar(256),
    foreign key (username) references users(username) ON DELETE CASCADE,
    foreign key (name) references dikumon(name) ON DELETE CASCADE
);
