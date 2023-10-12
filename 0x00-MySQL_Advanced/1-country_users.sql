-- Task: Create table 'users' with specified attributes and constraints

-- Create table 'users' if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    -- Define 'id' as an auto-incremented primary key
    id INT NOT NULL AUTO_INCREMENT,
    
    -- Define 'email' as a unique, not null column with a maximum length of 255 characters
    email VARCHAR(255) NOT NULL,
    
    -- Define 'name' as a VARCHAR(255) column
    name VARCHAR(255),
    
    -- Define 'country' as an ENUM column with allowed values ('US', 'CO', 'TN')
    -- Set 'US' as the default value
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US',
    
    -- Set 'id' as the primary key
    PRIMARY KEY (id),
    
    -- Enforce uniqueness on 'email' column
    UNIQUE (email)
);
