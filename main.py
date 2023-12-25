import cv2 as cv
import pg8000
import getpass
import json
from datetime import datetime

# Function to insert data into the PostgreSQL database
def insert_data(conn, name, image_data):
    try:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        cursor.execute("""
            INSERT INTO face_recognition.person_info (person_name, image_data, other_attributes, created_at)
            VALUES (%s, %s, %s::jsonb, %s)
        """, (name, image_data, json.dumps(other_attributes), timestamp))
        conn.commit()
        print("Data inserted successfully!")
    except pg8000.Error as e:
        print(f"Error inserting data: {e}")


# Function to capture and process images
def capture_images(conn):

    capture = cv.VideoCapture(0)  # Access to webcam

    # Load the Haar cascade for face detection
    haar_cascade = cv.CascadeClassifier('haar_face.xml')

    while True:
        is_true, frame = capture.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)

        for (x, y, w, h) in faces_rect:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

            # face region of interest
            face_roi = gray[y:y + h, x:x + w]

            # Prompt user for name
            name = input("Enter name for this face: ")

            # Convert the image to binary data
            _, img_encoded = cv.imencode('.jpg', face_roi)
            image_data = img_encoded.tobytes()

            # Insert the face data into the PostgreSQL database
            insert_data(conn, name, image_data)

        cv.imshow('Face Detection', frame)  # Display each frame of the video

        if cv.waitKey(20) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    capture.release()
    cv.destroyAllWindows()

# Function to access the database
def search(db):
    
    while True:
        choice = input('Search by face ID (F) or by name (N)?: ')
        if choice == 'F' or choice == 'f':
            id = input('Enter face ID: ')
            search_by_id(db, id) # implement this later
            break
        elif choice == 'N' or choice == 'n':
            name = input('Enter name (first and last): ')
            search_by_name(db, name) # implement this later
            break
        else:
            print('Invalid choice. Try again.')
        print(' ')

def alter(db):
    while True:
        choice = input('Add attributes (A), delete face (D)')
        if choice == 'A' or 'a':
            id = input('Enter face ID:')
            add_attribute(db, id) # implement this later
        elif choice == 'D' or choice == 'd':
            id = input('Enter face ID:')
            delete(db, id) # implement this later


# Connect to PostgreSQL database
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


# Main function to initiate the process
    
def main():
    # connect to the database. Loop until we get a db object.
    # This tells us that the user has successfully logged in.
    while True:
        db = get_connection()
        if db is not None:
            break

    # main loop
    while True:
        choice = input('Capture New Face (N)\nSearch Database (S)\nAlter Database (A)\nQuit (Q)\n')
        if choice == 'N' or choice == 'n':
            capture_images(db)
        elif choice == 'S' or choice == 's':
            search(db)
        elif choice == 'A' or choice == 'a':
            alter(db)
        elif (choice == 'Q' or choice == 'q'):
            print("Ending Session ... ")
            break
        else:
            print("Invalid choice. Try again.")
        print(" ")


if __name__ == "__main__":
    main()
