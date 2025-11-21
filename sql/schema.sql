CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    type ENUM("A", "H", "G") NOT NULL,

    PRIMARY KEY (user_id)
);

CREATE TABLE property (
    property_id INT NOT NULL AUTO_INCREMENT,
    host_id INT,

    title VARCHAR(255) NOT NULL,
    description VARCHAR(6000) NOT NULL,
    location VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,

    occupied BOOLEAN NOT NULL DEFAULT FALSE,
    rented_to INT,

    PRIMARY KEY (property_id),
    FOREIGN KEY (host_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (rented_to) REFERENCES users(user_id) ON DELETE SET NULL
);
