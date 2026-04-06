import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

brightness = 50

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image")
        break

    # rotation
    (h, w) = frame.shape[:2]

    center = (w//2, h//2)
    matrix = cv2.getRotationMatrix2D(center, 10, 1.0)
    frame = cv2.warpAffine(frame, matrix, (w,h))

    bright_frame = cv2.convertScaleAbs(frame, alpha=1, beta=brightness)

    gray = cv2.cvtColor (bright_frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,minSize=(30,30))
    
    for (x,y, w,h) in faces:
        cv2.rectangle(bright_frame, (x,y), (x+w, y+h), (255,0,0), 2)
        face_crop = bright_frame[y:y+h, x:x+w]

        cv2.imshow("Cropped Face", face_crop)

    cv2.putText(bright_frame, f"People Count: {len(faces)}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)

    cv2.imshow("Face Detection + Image Processing", bright_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    elif key == ord("+"):
        brightness += 10
    elif key == ord("-"):
        brightness -= 10

cap.release()
cv2.destroyAllWindows()