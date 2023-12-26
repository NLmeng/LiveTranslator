import pytesseract
from pytesseract import Output


def extract_text_and_boxes(image):
    """ Extract text and bounding boxes from an image using OCR. """
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    text_box_pairs = []
    for i in range(len(data['text'])):
        if data['text'][i].strip() != '':
            box = (data['left'][i], data['top'][i],
                   data['width'][i], data['height'][i])
            text_box_pairs.append((data['text'][i], box))
    return text_box_pairs
