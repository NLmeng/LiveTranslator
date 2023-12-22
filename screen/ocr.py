import pytesseract
from PIL import Image


def extract_text(image):
    """ Extract text from an image using OCR. """
    text = pytesseract.image_to_string(image)
    return text
