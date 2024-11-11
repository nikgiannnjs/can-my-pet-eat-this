CREATE TABLE animals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);


INSERT INTO animals (name) VALUES ('dog');
INSERT INTO animals (name) VALUES ('cat');
INSERT INTO animals (name) VALUES ('rabbit');
INSERT INTO animals (name) VALUES ('bird');
INSERT INTO animals (name) VALUES ('frog');
INSERT INTO animals (name) VALUES ('turtle');
INSERT INTO animals (name) VALUES ('fish');
INSERT INTO animals (name) VALUES ('snake');
INSERT INTO animals (name) VALUES ('spider');
INSERT INTO animals (name) VALUES ('hamster');
INSERT INTO animals (name) VALUES ('guinea pig');
INSERT INTO animals (name) VALUES ('lizard');
INSERT INTO animals (name) VALUES ('parrot');
INSERT INTO animals (name) VALUES ('gecko');
INSERT INTO animals (name) VALUES ('chinchilla');
INSERT INTO animals (name) VALUES ('ferret');
INSERT INTO animals (name) VALUES ('rat');
INSERT INTO animals (name) VALUES ('mouse');
INSERT INTO animals (name) VALUES ('hedgehog');
INSERT INTO animals (name) VALUES ('tortoise');
INSERT INTO animals (name) VALUES ('tarantula');
INSERT INTO animals (name) VALUES ('hermit crab');
INSERT INTO animals (name) VALUES ('gerbil');
INSERT INTO animals (name) VALUES ('salamander');


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(250) UNIQUE NOT NULL,
    email VARCHAR(250) UNIQUE NOT NULL,
    password_hash VARCHAR(250) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
)