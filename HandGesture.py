import cv2
import numpy as np


cap = cv2.VideoCapture(0)


if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()


while True:
    ret, frame = cap.read()


    if not ret:
        print("Error: Failed to capture image.")
        break


    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # Improved skin range
    lower_skin = np.array([0, 30, 60], dtype=np.uint8)
    upper_skin = np.array([20, 150, 255], dtype=np.uint8)


    # Mask
    mask = cv2.inRange(hsv, lower_skin, upper_skin)


    # 🔧 Noise removal
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)


    # 🔧 Blur
    mask = cv2.GaussianBlur(mask, (5,5), 0)


    result = cv2.bitwise_and(frame, frame, mask=mask)


    # Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    if contours:
        max_contour = max(contours, key=cv2.contourArea)


        if cv2.contourArea(max_contour) > 1000:
            x, y, w, h = cv2.boundingRect(max_contour)


            # Draw box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)


            # Center point
            cx = int(x + w/2)
            cy = int(y + h/2)
            cv2.circle(frame, (cx, cy), 50, (0,0,255), -1)


            # Label
            cv2.putText(frame, "Hand Detected", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)


    cv2.imshow("Original Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Filtered Frame", result)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
