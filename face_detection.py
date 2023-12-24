import cv2 as cv
import pg8000
import getpass

# Function to insert data into the PostgreSQL database
def insert_data(conn, name, image_data):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO faces_table (name, image) VALUES (%s, %s)", (name, image_data))
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
        'port': 5432,  # Change to your PostgreSQL port if different
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
    connection = get_connection()
    if connection:
        capture_images(connection)
        connection.close()

if __name__ == "__main__":
    main()
