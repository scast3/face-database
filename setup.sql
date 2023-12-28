SET search_path = public, face_recognition;

-- Host: localhost
-- Port: 5432
-- Username: postgres
-- TODO: make sure schema is good

-- Ideally, everyone's face will be in this table, need to make sure that these are the appropriate attributes
CREATE TABLE face_recognition.person_info (
    person_id SERIAL PRIMARY KEY,
    person_name VARCHAR(100) NOT NULL,
    image_data BYTEA NOT NULL, -- Assuming storing images as byte data
    other_attributes JSONB, -- You can store additional attributes in JSON format
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

