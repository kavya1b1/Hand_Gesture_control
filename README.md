🤟 Hand Gesture Control System (MacOS)
This project uses your webcam and MediaPipe to detect hand gestures and control system functions on macOS such as volume, music playback (Spotify), screenshots, locking the screen, and opening Finder.

✨ Features

✋ Mute & Unmute with Fist

🔊 Volume Control with Middle Finger / Thumb Down

⏯ Play/Pause (Spotify) using Peace Sign

⏭/⏮ Swipe Right/Left for Next/Previous Spotify Track

📂 Open Finder with "Call Me" Gesture

🖼️ Take Screenshot using Thumb + Index Gesture

🔒 Lock Screen with 4 Fingers Up, Thumb Down


🧠 How It Works

Uses MediaPipe for real-time hand tracking and gesture recognition. The gestures are mapped to Mac-specific actions via AppleScript.

🛠️ Requirements

macOS

Python 3.7+

pip

🔧 Installation

Clone this repo and install dependencies:

git clone [https://github.com/kavya1b1/hand-gesture-mac-control.git](https://github.com/kavya1b1/Hand_Gesture_control/blob/main/hand_gesture_control.py)
cd hand-gesture-mac-control
pip install opencv-python mediapipe numpy

⚙️ Run the App

python3 gesture_control.py

🙌 Supported Gestures

Gesture	Action
Fist	Mute / Unmute
Middle Finger Up	Volume Up
Thumb Down	Volume Down
Peace Sign	Spotify Play/Pause
Call Me Sign	Open Finder
Thumb + Index	Take Screenshot
Swipe Right	Next Track
Swipe Left	Previous Track
4 Fingers Up	Lock Screen

📁 File Structure

gesture_control.py # Main script
assets/ # (Optional) Store images or demo gifs
README.md # This file

📌 Notes

Only works on macOS due to AppleScript dependencies.

Uses system volume and controls Spotify app directly.

Screenshot is saved to Desktop.
