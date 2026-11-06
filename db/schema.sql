CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Files (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    size INTEGER,
    location VARCHAR(255),
    owner_id INT REFERENCES Users(id)
);

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'op_type') THEN
        CREATE TYPE op_type AS ENUM ('create', 'modify', 'delete', 'read');
    END IF;
END$$;

CREATE TABLE IF NOT EXISTS Operations (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operation_type op_type,
    file_id INT REFERENCES Files(id),
    user_id INT REFERENCES Users(id)
);