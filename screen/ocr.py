import pytesseract
from pytesseract import Output


def extract_text_and_boxes(image, lang='eng', psm=6):
    """ Extract text and bounding boxes from an image using OCR. """
    config = f'--psm {psm} --oem 3 -l {lang}'
    data = pytesseract.image_to_data(image, config=config, output_type=Output.DICT)
    text_box_pairs = []
    for i in range(len(data['text'])):
        if data['text'][i].strip() != '':
            box = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            text_box_pairs.append((data['text'][i], box))
    return text_box_pairs
