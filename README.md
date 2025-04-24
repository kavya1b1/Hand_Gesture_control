# Hand_Gesture_control

# 🖐️ Hand Gesture Control for macOS

Control your Mac using simple hand gestures detected via webcam! This project uses **MediaPipe** and **OpenCV** to recognize gestures and trigger useful macOS actions like adjusting volume, locking the screen, controlling Spotify, and more.

## 🚀 Features

- ✊ **Mute/Unmute** — Make a fist to mute, release to unmute
- ✌️ **Play/Pause Spotify** — Use a peace sign
- 🤙 **Open Finder** — Show a "Call me" sign
- 👍 **Take Screenshot** — Thumb + index up, others down
- 🖕 **Volume Up** — Raise only your middle finger
- 👎 **Volume Down** — Point thumb downward
- 🖐️ **Lock Screen** — All fingers up

## 🧠 Technologies Used

- **Python**
- **MediaPipe** – Hand tracking
- **OpenCV** – Webcam input and gesture drawing
- **AppleScript (osascript)** – Trigger macOS actions
- **Subprocess** – Run shell commands

## 🖥️ Prerequisites

- macOS
- Python 3.7+
- Webcam

Install dependencies:


```bash
pip install opencv-python mediapipe numpy
