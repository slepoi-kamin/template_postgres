CREATE TABLE users
(
    id SERIAL NOT NULL ,
    chat_id INT,
    username  VARCHAR(120),
    full_name VARCHAR(120),
    PRIMARY KEY (id)
);
