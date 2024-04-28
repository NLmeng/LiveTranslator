import cv2
from PIL import ImageGrab


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

def put_text_on_frame(frame, text, box, font_scale=0.5, font_thickness=1, draw_box=False):
    """ Puts text on the frame image with a blurred background for the text box and optionally draws the bounding box. """
    x, y, w, h = box
    frame = blur_background(frame, box)

    if draw_box:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 

    text_size = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
    text_x = x + (w - text_size[0]) // 2
    text_y = y + (h + text_size[1]) // 2

    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)
