import cv2
import mediapipe as mp
import numpy as np
import subprocess
import time
import os

def set_volume_mac(volume):
    volume = max(0, min(100, volume))
    subprocess.run(["osascript", "-e", f"set volume output volume {volume}"], check=True)

def get_volume_mac():
    result = subprocess.run(["osascript", "-e", "output volume of (get volume settings)"], capture_output=True, text=True)
    return int(result.stdout.strip())

# Spotify Controlss
def play_pause():
    subprocess.run(["osascript", "-e", 'tell application "Spotify" to playpause'])

def next_track():
    subprocess.run(["osascript", "-e", 'tell application "Spotify" to next track'])

def prev_track():
    subprocess.run(["osascript", "-e", 'tell application "Spotify" to previous track'])

# Finder
def open_finder():
    subprocess.run(["osascript", "-e", 'tell application "Finder" to activate'])

# Screenshot (fix)
def take_screenshot():
    timestamp = int(time.time())
    filepath = os.path.expanduser(f"~/Desktop/screenshot_{timestamp}.png")
    subprocess.run(["screencapture", filepath])
    print(f"Screenshot saved: {filepath}")

# Lock screen (new gesture logic)
def lock_screen():
    subprocess.run(["pmset", "displaysleepnow"])

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

mute_state = False
was_fist_detected = False
last_action_time = 0

prev_index_x = None
swipe_cooldown = 1  # seconds

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    detected_gesture = None
    is_fist_detected = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            finger_tips = [8, 12, 16, 20]
            finger_bases = [6, 10, 14, 18]

            index_tip_x = landmarks[8].x  # for swipe

            # Fist Detection
            is_fist = all(landmarks[tip].y > landmarks[base].y for tip, base in zip(finger_tips, finger_bases))
            if is_fist:
                is_fist_detected = True

            # Screenshot Gesture: Only Thumb + Index up
            if landmarks[4].y < landmarks[3].y and landmarks[8].y < landmarks[6].y and \
               all(landmarks[tip].y > landmarks[base].y for tip, base in zip([12, 16, 20], [10, 14, 18])):
                detected_gesture = "screenshot"

            # Play/Pause Gesture: Peace sign
            elif landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and \
                 all(landmarks[tip].y > landmarks[base].y for tip, base in zip([16, 20], [14, 18])):
                detected_gesture = "play_pause"

            # Finder Gesture: Call me sign
            elif landmarks[4].y < landmarks[3].y and landmarks[20].y < landmarks[18].y and \
                 all(landmarks[tip].y > landmarks[base].y for tip, base in zip([8, 12, 16], [6, 10, 14])):
                detected_gesture = "finder"

            # Volume Up - Middle finger only
            elif sum(1 for tip, base in zip(finger_tips, finger_bases) if landmarks[tip].y < landmarks[base].y) == 1 and \
                 landmarks[12].y < landmarks[10].y:
                detected_gesture = "volume_up"

            # Volume Down - Thumb down
            elif landmarks[4].y > landmarks[3].y and all(landmarks[tip].y > landmarks[base].y for tip in [8, 12, 16, 20] for base in [6, 10, 14, 18]):
                detected_gesture = "volume_down"

            # Lock screen - Only 4 fingers up (thumb down)
            elif all(landmarks[tip].y < landmarks[base].y for tip, base in zip(finger_tips, finger_bases)) and \
                 landmarks[4].y > landmarks[3].y:
                detected_gesture = "lock"

            # Swipe Gestures for Next/Prev Track
            if prev_index_x is not None:
                movement = index_tip_x - prev_index_x
                if movement > 0.2:
                    detected_gesture = "next"
                elif movement < -0.2:
                    detected_gesture = "previous"
            prev_index_x = index_tip_x

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Mute Toggle
    if is_fist_detected and not was_fist_detected:
        set_volume_mac(0)
        mute_state = True
    elif not is_fist_detected and was_fist_detected:
        set_volume_mac(50)
        mute_state = False
    was_fist_detected = is_fist_detected

    # Cooldown
    current_time = time.time()
    if detected_gesture and (current_time - last_action_time) > 0.8:
        last_action_time = current_time

        if detected_gesture == "volume_up":
            set_volume_mac(get_volume_mac() + 5)

        elif detected_gesture == "volume_down":
            set_volume_mac(get_volume_mac() - 5)

        elif detected_gesture == "play_pause":
            play_pause()

        elif detected_gesture == "finder":
            open_finder()

        elif detected_gesture == "screenshot":
            take_screenshot()

        elif detected_gesture == "lock":
            lock_screen()

        elif detected_gesture == "next":
            next_track()

        elif detected_gesture == "previous":
            prev_track()

    # Display
    if mute_state:
        cv2.putText(frame, "MUTED", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    elif detected_gesture:
        cv2.putText(frame, detected_gesture.upper(), (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




