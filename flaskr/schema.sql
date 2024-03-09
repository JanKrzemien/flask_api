DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS model;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

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

CREATE TABLE model (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(75) NOT NULL,
    release_date DATE NOT NULL,
    specs VARCHAR(1000)
);

CREATE TABLE device (
    serial_number VARCHAR(20) PRIMARY KEY,
    model_id INTEGER NOT NULL,
    production_date DATE NOT NULL,
    last_serviced DATE,
    battery DECIMAL(2, 2),
    status_id INTEGER NOT NULL,
    location_id INTEGER,
    other_info VARCHAR(200),
    FOREIGN KEY (model_id) REFERENCES model (id),
    FOREIGN KEY (status_id) REFERENCES status (id),
    FOREIGN KEY (location_id) REFERENCES location (id)
);
