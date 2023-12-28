import cv2 as cv
import pg8000
from datetime import datetime
import getpass
# testing inserting items/images into the db


def get_connection() -> pg8000.Connection:
    # Get the username and password
    username = input('Username: ')
    password = getpass.getpass('Password: ')

    # Connect to the database
    credentials = {
        'user': username,
        'password': password,
        'database': 'faces',
        'port': 5432,
        'host': 'localhost'
    }
    try:
        db = pg8000.connect(**credentials)
        db.autocommit = False
        return db
    except pg8000.Error as e:
        print(f'Authentication failed for user "{username}" (error: {e})\n')
        return None

# establish connection to database
conn = get_connection()

# image from test folder
image = cv.imread('test images/vader.jpg')

# Convert image to binary format
_, image_binary = cv.imencode('.jpg', image)
image_binary_data = image_binary.tobytes()

# SQL query
sql = """
    INSERT INTO face_recognition.person_info (person_name, image_data, other_attributes, created_at)
    VALUES (%s, %s, %s, %s)
"""

cursor = conn.cursor()
cursor.execute(sql, ('Test Person', image_binary_data, '{}', datetime.now()))
conn.commit()
conn.close()

print("Insertion was successful")