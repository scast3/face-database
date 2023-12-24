import cv2 as cv
import pg8000

import getpass

from pg8000 import Connection, Cursor
from typing import List, Tuple, Optional

# live webcam face detection

# connect to postgres database
def get_connection() -> Optional[Connection]:
    """
    Creates a connection to the database
    """
    # get the username and password
    username = input('Username: ')
    password = getpass.getpass('Password: ')

    # connect to the database
    credentials = {
        'user': username,
        'password': password,
        'database': 'faces',
        'port': 5433,
        'host': 'localhost'
    }
    try:
        db = pg8000.connect(**credentials)
        # do not change the autocommit line below or set autocommit to true in your solution
        # this lab requires you add appropriate db.commit() calls
        db.autocommit = False
    except pg8000.Error as e:
        print(f'Authentication failed for user "{username}" (error: {e})\n')
        return None

    return db

capture = cv.VideoCapture(0) # access to webcam

haar_cascade = cv.CascadeClassifier('haar_face.xml')

while True:
    isTrue, frame = capture.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) 
    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1) 

    for (x,y,w,h) in faces_rect:
        cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), thickness=2)

    cv.imshow('Face Detection', frame) #displays each frame of the video

    if cv.waitKey(20) & 0xFF==ord('d'): #if the letter d is pressed, stop displaying video
        break
capture.release()
cv.destroyAllWindows()