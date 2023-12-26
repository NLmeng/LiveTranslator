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
    text_box_pairs = []
    for i in range(len(data['text'])):
        if data['text'][i].strip() != '':  # Filter out empty strings
            box = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            text_box_pairs.append((data['text'][i], box))
    return text_box_pairs

def put_number_on_frame(frame, number, box, font_scale=0.5, font_thickness=1):
    """ Puts a numbered label on the frame image. """
    x, y, w, h = box
    # Draw a rectangle around the text
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # Position for the number label
    label_position = (x, y - 10)
    # Put the number on the frame
    cv2.putText(frame, str(number), label_position, cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, (0, 0, 255), font_thickness, cv2.LINE_AA)

def startMock():
    """ Process a single frame, draw numbered boxes, print texts, and save the image. """
    screenshot = capture_screenshot()  # Capture one screenshot
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    text_box_pairs = extract_text_and_boxes(screenshot)  # Perform OCR

    for number, (text, box) in enumerate(text_box_pairs, start=1):
        print(f"Box {number}: {text}")  # Print text with box number
        put_number_on_frame(frame, number, box, font_scale=0.5,
                            font_thickness=1)  # Overlay text number

    cv2.imwrite("annotated_frame.jpg", frame)
