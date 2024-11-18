CREATE TABLE animals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(250) UNIQUE NOT NULL,
    email VARCHAR(250) UNIQUE NOT NULL,
    password_hash VARCHAR(250) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
    password_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE pets(
    id SERIAL PRIMARY KEY,
    name VARCHAR(250) NOT NULL, 
    weight DECIMAL(3,1) NOT NULL, 
    user_id INT REFERENCES users(id) ON DELETE CASCADE, 
    animal_id INT REFERENCES animals(id) ON DELETE CASCADE, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

CREATE TABLE foods(
    id SERIAL PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE edibility(
    id SERIAL PRIMARY KEY,
    food_id INT REFERENCES foods(id) ON DELETE CASCADE,
    animal_id INT REFERENCES animals(id) ON DELETE CASCADE,
    can_eat BOOLEAN NOT NULL,
    notes VARCHAR(500)
)

--animals table seed
INSERT INTO animals (name) VALUES 
('dog'),
('cat'),
('rabbit'),
('bird'),
('frog'),
('turtle')

--foods table seed
INSERT INTO foods (name) VALUES 
('apple'),
('banana'),
('carrot'),
('chocolate'),
('onions')


--edibility table seed
INSERT INTO edibility (food_id, animal_id, can_eat, notes) VALUES
(1, 1, TRUE, 'Dogs can eat apples in moderation, remove seeds'),
(1, 2, TRUE, 'Cats can eat apples in small amounts'),
(1, 3, TRUE, 'Rabbits can eat apples in moderation'),
(1, 4, TRUE, 'Birds can eat apples, avoid seeds'),
(1, 5, TRUE, 'Frogs can eat apples in small amounts'),
(1, 6, TRUE, 'Turtles can eat apples in moderation'),
(2, 1, TRUE, 'Dogs can eat bananas in moderation'),
(2, 2, TRUE, 'Cats can eat bananas in moderation'),
(2, 3, TRUE, 'Rabbits can eat bananas in moderation'),
(2, 4, TRUE, 'Birds can eat bananas in moderation'),
(2, 5, TRUE, 'Frogs can eat bananas in small amounts'),
(2, 6, TRUE, 'Turtles can eat bananas in small amounts'),
(3, 1, TRUE, 'Dogs can eat carrots in moderation'),
(3, 2, TRUE, 'Cats can eat carrots in small amounts'),
(3, 3, TRUE, 'Rabbits can eat carrots, great source of vitamin A'),
(3, 4, TRUE, 'Birds can eat carrots in moderation'),
(3, 5, TRUE, 'Frogs can eat carrots in small amounts'),
(3, 6, TRUE, 'Turtles can eat carrots in moderation'),
(4, 1, FALSE, 'Dogs cannot eat chocolate as it is toxic to them'),
(4, 2, FALSE, 'Cats cannot eat chocolate as it is toxic to them'),
(4, 3, FALSE, 'Rabbits cannot eat chocolate, toxic to them'),
(4, 4, FALSE, 'Birds cannot eat chocolate, toxic to them'),
(4, 5, FALSE, 'Frogs cannot eat chocolate, toxic to them'),
(4, 6, FALSE, 'Turtles cannot eat chocolate, toxic to them'),
(5, 1, FALSE, 'Dogs cannot eat onions as it is toxic to them'),
(5, 2, FALSE, 'Cats cannot eat onions as it is toxic to them'),
(5, 3, FALSE, 'Rabbits cannot eat onions, toxic to them'),
(5, 4, FALSE, 'Birds cannot eat onions, toxic to them'),
(5, 5, FALSE, 'Frogs cannot eat onions, toxic to them'),
(5, 6, FALSE, 'Turtles cannot eat onions, toxic to them');