DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  admin BIT NOT NULL,
  refresh_secret_key TEXT UNIQUE NOT NULL
);

CREATE TABLE status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message VARCHAR(150) NOT NULL,
    color VARCHAR(25) NOT NULL
);

CREATE TABLE device (
    serial_number VARCHAR(20) PRIMARY KEY,
    production_date DATE NOT NULL,
    last_serviced DATE,
    battery DECIMAL(2, 2),
    status_id INTEGER NOT NULL,
    other_info VARCHAR(200),
    latitude DECIMAL(23, 20),
    longitude FLOAT(23, 20),
    FOREIGN KEY (status_id) REFERENCES status (id)
);
