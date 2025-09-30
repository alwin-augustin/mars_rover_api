CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    sol INTEGER,
    camera_name VARCHAR(50),
    img_src TEXT,
    earth_date DATE,
    rover_name VARCHAR(50)
);