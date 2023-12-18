import time

import cv2
import numpy as np
from PIL import ImageGrab


def capture_screenshot(region=None):
    """ Capture a screenshot. If region is provided, captures a specific area. """
    screen = ImageGrab.grab(bbox=region)
    return screen


def continuous_capture(interval=2):
    """ Continuously capture the screen at a specified interval (in seconds). """
    while True:
        screenshot = capture_screenshot()
        # Yield the screenshot for external use
        yield screenshot
        time.sleep(interval)


def start():
    """
    Start the continuous screen capture process.
    Displays each captured screenshot in an OpenCV window and allows the user to exit by pressing 'q'.
    The screen is captured every 2 seconds by default (adjustable in continuous_capture).
    """
    # Create a window for display using OpenCV
    cv2.namedWindow("Screenshot", cv2.WINDOW_NORMAL)

    for screenshot in continuous_capture():
        # Convert the PIL Image (screenshot) to a NumPy array for OpenCV compatibility
        frame = np.array(screenshot)

        # Convert color space from RGB (PIL) to BGR (OpenCV)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.imshow("Screenshot", frame)
        if cv2.waitKey(500) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
