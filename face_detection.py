import cv2 as cv
# live webcam face detection

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