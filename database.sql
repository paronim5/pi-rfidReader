CREATE TABLE users (
    rfid_card_id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    surname VARCHAR NOT NULL,
    email VARCHAR,
    phone VARCHAR,
    created_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP),
    PRIMARY KEY (rfid_card_id)
);

CREATE TABLE visits (
    id INTEGER NOT NULL,
    rfid_card_id VARCHAR NOT NULL,
    arrived_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP),
    departed_at TIMESTAMP NULL,  -- Nullable column for departure time
    PRIMARY KEY (id),
    FOREIGN KEY(rfid_card_id) REFERENCES users (rfid_card_id)
);
