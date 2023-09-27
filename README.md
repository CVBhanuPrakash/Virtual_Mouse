# Virtual Mouse with Hand Gestures

## Overview

This project is a virtual mouse that allows you to control your computer's mouse cursor using hand gestures captured by your webcam. It leverages the following Python libraries and modules: `cv2`, `numpy`, `time`, `autopy`, `mediapipe`, `math`, and `webbrowser`.

## Supported Hand Gestures

### Scroll Up
- If the forefinger and little finger are both raised, the virtual mouse will scroll up.

### Scroll Down
- When the forefinger, little finger, and thumb are all raised simultaneously, the virtual mouse will scroll down.

### Volume Down
- Raising the thumb and index finger while keeping other fingers down will lower the volume on your computer.

### Volume Up
- Lowering the thumb while keeping all other fingers raised will increase the volume.

### Open Website
- Raising the forefinger, middle finger, and ring finger (three fingers) will trigger the virtual mouse to open a predefined website.

### Click
- If the forefinger and middle finger are both raised, the virtual mouse will simulate a mouse click action.

## How to Use

1. Ensure that your computer has a webcam.

2. Run the Python script provided in this project.

3. Position your hand in front of the webcam and make the desired gestures according to the supported actions listed above.

4. The virtual mouse will interpret your gestures and perform the corresponding actions on your computer.

## Dependencies

This project relies on the following Python libraries and modules:

- `cv2` for computer vision and hand tracking.
- `numpy` for numerical operations.
- `time` for time-related functions.
- `autopy` for simulating mouse and keyboard input.
- `mediapipe` for hand tracking and gesture recognition.
- `math` for mathematical calculations.
- `webbrowser` for opening websites in the default web browser.

## Usage

Feel free to explore the code provided in this repository to understand how the virtual mouse is implemented. You can also customize the gestures and actions according to your preferences.

## License

This project is open-source and available under the [MIT License](LICENSE). You are welcome to use, modify, and distribute it as you see fit.
