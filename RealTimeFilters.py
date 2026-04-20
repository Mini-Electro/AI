import cv2
import mediapipe as mp
import numpy as np
import math
import os
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

save_folder = "captured_images"
os.makedirs(save_folder, exist_ok=True)

current_filter = "Normal"
last_capture_time = 0
capture_cooldown = 1.5
last_gesture_time = 0
gesture_cooldown = 0.8

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def apply_filter(frame, filter_name):
    if filter_name == "Grayscale":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    elif filter_name == "Sepia":
        kernel = np.array([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]
        ])
        sepia = cv2.transform(frame, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)

    elif filter_name == "Negative":
        return cv2.bitwise_not(frame)

    elif filter_name == "Blur":
        return cv2.GaussianBlur(frame, (21, 21), 0)

    return frame

def save_image(frame):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_folder, f"photo_{timestamp}.jpg")
    cv2.imwrite(filename, frame)
    print(f"Saved: {filename}")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    display_frame = frame.copy()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture_text = "No Hand Detected"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(display_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape

            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            ring_tip = hand_landmarks.landmark[16]
            pinky_tip = hand_landmarks.landmark[20]

            thumb_point = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_point = (int(index_tip.x * w), int(index_tip.y * h))
            middle_point = (int(middle_tip.x * w), int(middle_tip.y * h))
            ring_point = (int(ring_tip.x * w), int(ring_tip.y * h))
            pinky_point = (int(pinky_tip.x * w), int(pinky_tip.y * h))

            touch_threshold = 40

            thumb_index_dist = distance(thumb_point, index_point)
            thumb_middle_dist = distance(thumb_point, middle_point)
            thumb_ring_dist = distance(thumb_point, ring_point)
            thumb_pinky_dist = distance(thumb_point, pinky_point)

            current_time = time.time()

            if thumb_index_dist < touch_threshold:
                gesture_text = "Capture Gesture"
                if current_time - last_capture_time > capture_cooldown:
                    filtered_frame = apply_filter(frame.copy(), current_filter)
                    save_image(filtered_frame)
                    last_capture_time = current_time

            elif thumb_middle_dist < touch_threshold:
                gesture_text = "Grayscale Gesture"
                if current_time - last_gesture_time > gesture_cooldown:
                    current_filter = "Grayscale"
                    last_gesture_time = current_time

            elif thumb_ring_dist < touch_threshold:
                gesture_text = "Sepia Gesture"
                if current_time - last_gesture_time > gesture_cooldown:
                    current_filter = "Sepia"
                    last_gesture_time = current_time

            elif thumb_pinky_dist < touch_threshold:
                gesture_text = "Negative Gesture"
                if current_time - last_gesture_time > gesture_cooldown:
                    current_filter = "Negative"
                    last_gesture_time = current_time

            else:
                gesture_text = "No Touch Gesture"

    filtered_display = apply_filter(display_frame, current_filter)

    cv2.putText(filtered_display, f"Filter: {current_filter}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(filtered_display, f"Gesture: {gesture_text}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    cv2.putText(filtered_display, "Thumb+Index = Capture", (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.putText(filtered_display, "Thumb+Middle = Grayscale", (10, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.putText(filtered_display, "Thumb+Ring = Sepia", (10, 170),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.putText(filtered_display, "Thumb+Pinky = Negative", (10, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow("Gesture Controlled Photo App", filtered_display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("b"):
        current_filter = "Blur"
    elif key == ord("n"):
        current_filter = "Normal"

cap.release()
cv2.destroyAllWindows()