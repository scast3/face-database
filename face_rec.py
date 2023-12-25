import cv2 as cv

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

# Function to recognize a face using the faces from the database
# TODO implement this

def face_recognition(db):
    print('recognize face')