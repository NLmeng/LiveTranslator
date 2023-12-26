import time

import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab
from pytesseract import Output


def capture_screenshot(region=None):
    """ Capture a screenshot. If region is provided, captures a specific area. """
    screen = ImageGrab.grab(bbox=region)
    return screen


def extract_text_and_boxes(image):
    """ Extract text and bounding boxes from an image using OCR. """
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    boxes = [(data['left'][i], data['top'][i], data['width'][i], data['height'][i])
             for i in range(len(data['text'])) if data['text'][i].strip() != '']
    return data['text'], boxes


def put_number_on_frame(frame, number, box, font_scale=0.5, font_thickness=1):
    """ Puts a numbered label on the frame image. """
    x, y, w, h = box
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    label_position = (x + int(w/10), y + int(h/2))
    cv2.putText(frame, str(number), label_position, cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, (0, 0, 255), font_thickness, cv2.LINE_AA)


def startMock():
    """ Process a single frame, draw numbered boxes, print texts, and save the image. """
    screenshot = capture_screenshot()  # Capture one screenshot
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    texts, boxes = extract_text_and_boxes(screenshot)  # Perform OCR

    for number, (text, box) in enumerate(zip(texts, boxes), start=1):
        print(f"Box {number}: {text}")
        put_number_on_frame(frame, number, box, font_scale=0.5,
                            font_thickness=1)  # Overlay text number

    cv2.imwrite("annotated_frame.jpg", frame)
