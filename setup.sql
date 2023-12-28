SET search_path = public, face_recognition;

-- Host: localhost
-- Port: 5432
-- Username: postgres
-- TODO: make sure schema is good

-- Schema Design:
-- 2 main tables, photo_info stores all photos
-- person stores each individual person in the database

-- Ideally, everyone's face will be in this table, need to make sure that these are the appropriate attributes
CREATE TABLE face_recognition.photo_info (
    photo_id SERIAL PRIMARY KEY, -- unique to each photo
    person_id -- references people.person_id, assigned by user specification
    image_data BYTEA NOT NULL, -- Assuming storing images as byte data
    other_attributes JSONB, -- You can store additional attributes in JSON format
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add another table for each unique person
CREATE TABLE face_recognition.person (
    person_id SERIAL PRIMARY KEY,
    person_name VARCHAR(100) NOT NULL,
    primary_photo BYTEA NOT NULL,
    has_permission BOOLEAN,
    notes JSONB,
    user, -- allow user to set username and password ??? potentially
    pass, 
)