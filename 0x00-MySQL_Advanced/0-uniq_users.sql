-- Task: Create table 'users' with specified attributes and constraints

-- Create table 'users' if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    -- Define 'id' as an auto-incremented primary key
    id INT NOT NULL AUTO_INCREMENT,
    
    -- Define 'email' as a unique, not null column
    email VARCHAR(255) NOT NULL,
    
    -- Define 'name' as a VARCHAR(255) column
    name VARCHAR(255),
    
    -- Set 'id' as the primary key
    PRIMARY KEY (id),
    
    -- Enforce uniqueness on 'email' column
    UNIQUE (email)
);
