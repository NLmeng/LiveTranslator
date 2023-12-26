import cv2
import numpy as np
from PIL import ImageGrab

from .ocr import extract_text_and_boxes


def capture_screenshot(region=None):
    """ Capture a screenshot. If region is provided, captures a specific area. """
    screen = ImageGrab.grab(bbox=region)
    return screen


def blur_background(frame, box):
    """ Apply a blur effect to the background of a bounding box. """
    x, y, w, h = box
    blurred_box = cv2.GaussianBlur(
        frame[y:y+h, x:x+w], (15, 15), cv2.BORDER_DEFAULT)
    frame[y:y+h, x:x+w] = blurred_box
    return frame


def put_text_on_frame(frame, text, box, font_scale=0.5, font_thickness=1):
    """ Puts text on the frame image with a blurred background for the text box. """
    x, y, w, h = box
    frame = blur_background(frame, box)

    text_size = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
    text_x = x + (w - text_size[0]) // 2
    text_y = y + (h + text_size[1]) // 2

    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)


def startMock():
    """ Process a single frame, overlay text with blurred background, and save the image. """
    screenshot = capture_screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    text_box_pairs = extract_text_and_boxes(screenshot)

    for text, box in text_box_pairs:
        put_text_on_frame(frame, text, box, font_scale=0.5, font_thickness=1)

    cv2.imwrite("annotated_frame.jpg", frame)
