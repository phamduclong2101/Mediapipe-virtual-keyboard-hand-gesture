# Mediapipe Virtual Keyboard Hand Gesture

This project uses the **Mediapipe** library to recognize hand gestures and create a virtual keyboard, where users can type text by moving their index finger and middle finger. When these two fingers move close to each other, a key on the virtual keyboard will be "pressed."

## Description

- The project uses **Mediapipe** to recognize hands and the landmarks of the hand.
- When the index and middle fingers are close together (below a certain threshold), the system recognizes that the user has pressed a key on the virtual keyboard.
- The virtual keyboard includes letter keys, punctuation, and the **Space** key for inserting spaces.
- Additionally, the **Backspace (<)** key can be used to delete the last entered character.

## Required Libraries

This project requires the following libraries:

- `opencv-python`: A library for image and video processing.
- `mediapipe`: A library for recognizing gestures and objects in images.
- `pynput`: A library for controlling the virtual keyboard.

### Installing Libraries

To install the required libraries, you can create a virtual environment and install them via `pip`:

```bash
pip install -r requirements.txt
