DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS model;

CREATE TABLE location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude DECIMAL(23, 20),
    longitude FLOAT(23, 20)
);

CREATE TABLE status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message VARCHAR(150) NOT NULL,
    color VARCHAR(25) NOT NULL
);

CREATE TABLE model {
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(75) NOT NULL,
    release_date DATE NOT NULL,
    specs VARCHAR(1000)
};

CREATE TABLE device (
    serial_number VARCHAR(20) PRIMARY KEY AUTOINCREMENT,
    FOREIGN KEY (model_id) REFERENCES model (id) NOT NULL,
    production_date DATE NOT NULL,
    last_serviced DATE,
    battery DECIMAL(2, 2),
    FOREIGN KEY (status_id) REFERENCES status (id) NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location (id),
    other_info VARCHAR(200)
);
