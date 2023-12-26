import pytesseract
from PIL import Image


def extract_text(image):
    """ Extract text from an image using OCR. """
    text = pytesseract.image_to_string(image)
    return text


def extract_text_and_boxes(image):
    """ Extract text and bounding boxes from an image using OCR. """
    data = pytesseract.image_to_data(
        image, output_type=pytesseract.Output.DICT)

    text_list = data['text']
    boxes = [(data['left'][i], data['top'][i], data['width'][i], data['height'][i])
             for i in range(len(data['text'])) if data['text'][i].strip() != '']

    return text_list, boxes
