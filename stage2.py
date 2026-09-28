import cv2
import math
import mediapipe as mp
from fingers import get_fingers_up
from actions import classify, trigger, update_volume_from_distance

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )
            lm = hand_landmarks.landmark
            fingers = get_fingers_up(lm)
                        # Pinch distance for volume control
            h, w, _ = frame.shape
            thumb = lm[4]
            index = lm[8]
            x1, y1 = int(thumb.x * w), int(thumb.y * h)
            x2, y2 = int(index.x * w), int(index.y * h)
            distance = math.hypot(x2 - x1, y2 - y1)

            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(frame, (x1, y1), 8, (255, 0, 255), -1)
            cv2.circle(frame, (x2, y2), 8, (255, 0, 255), -1)
            count = sum(fingers)

            cv2.putText(frame, f"{fingers}  count={count}", (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            gesture = classify(fingers)
            trigger(gesture)
            gesture = classify(fingers)

            # Volume mode: thumb+index free, other fingers curled
            if fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                vol = update_volume_from_distance(distance)
                if vol is not None:
                    cv2.putText(frame, f"Volume: {int(vol)}%", (20, 140),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            else:
                trigger(gesture)

            cv2.putText(frame, f"Gesture: {gesture}", (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.putText(frame, f"Gesture: {gesture}", (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()