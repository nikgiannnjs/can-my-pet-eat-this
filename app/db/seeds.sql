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

CREATE TABLE terms_of_service (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tos_acceptance (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    tos_id INT REFERENCES terms_of_service(id) ON DELETE CASCADE,
    accepted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id , tos_id)
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE user_roles (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    role_id INT REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);


--animals table seed
INSERT INTO animals (name) VALUES 
('Dog'),
('Cat'),
('Rabbit'),
('Bird'),
('Frog'),
('Turtle')

--foods table seed
INSERT INTO foods (name) VALUES 
('Apple'),
('Banana'),
('Carrot'),
('Chocolate'),
('Onions')


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

--terms_of_service seed
INSERT INTO terms_of_service (version, content) VALUES
('1.1' , 'Welcome to Can My Pet Eat That. By accessing or using our service, you agree to our terms and conditions')

--roles seed
INSERT INTO roles (name) VALUES 
('common user' , 'admin' , 'veterinarian')

--Manual admin role seed
INSERT INTO user_roles (user_id , role_id) VALUES
(your_user_id , admin_id)