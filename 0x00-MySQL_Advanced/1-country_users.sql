-- creates a table users
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    country ENUM('US','CO','TN') NOT NULL DEFAULT 'US',
    UNIQUE(email)
)
