import os
import requests
import psycopg2

def get_photos():
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos"
    params = {
        "api_key": "7aFUsY9tDWojoOqYAkvDLlH4KoykvxG6mCqES28F"
    }

    response = requests.get(url, params=params)
    return response.json()

def save_photos(photos, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for photo in photos:
        year = photo['earth_date'].split('-')[0]
        month = photo['earth_date'].split('-')[1]
        day = photo['earth_date'].split('-')[2]
        file_name = photo['img_src'].split('/')[-1]
        directory_path = os.path.join(directory, str(photo['earth_date']), year, month, day)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        img_url = photo['img_src']
        img_data = requests.get(img_url).content
        img_name = os.path.join(directory_path, file_name)
        with open(img_name, 'wb') as img_file:
            img_file.write(img_data)

def insert_photo_metadata(photo, db_connection):
    cursor = db_connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INT PRIMARY KEY,
            sol INT,
            camera_name VARCHAR(255),
            img_src VARCHAR(255),
            earth_date DATE,
            rover_name VARCHAR(255)
        );
    """)
    cursor.execute("""
        INSERT INTO photos (id, sol, camera_name, img_src, earth_date, rover_name)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        photo['id'],
        photo['sol'],
        photo['camera']['full_name'],
        photo['img_src'],
        photo['earth_date'],
        photo['rover']['name']
    ))
    db_connection.commit()

def get_photos_metadata(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM photos")
    return cursor.fetchall()

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )

def main():
    db_connection = get_db_connection()
    photos_data = get_photos()
    latest_photos = photos_data.get('latest_photos', [])
    
    if latest_photos:
        save_photos(latest_photos, 'downloads')
        for photo in latest_photos:
            insert_photo_metadata(photo, db_connection)
    photo_metadata = get_photos_metadata(db_connection)
    for metadata in photo_metadata:
        print(metadata)
    db_connection.close()

if __name__ == "__main__":
    main()
