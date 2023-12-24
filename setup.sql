SET search_path = public, face_recognition;


CREATE TABLE face_recognition.person_info (
    person_id SERIAL PRIMARY KEY,
    person_name VARCHAR(100) NOT NULL,
    image_data BYTEA NOT NULL, -- Assuming storing images as byte data
    other_attributes JSONB, -- You can store additional attributes in JSON format
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

