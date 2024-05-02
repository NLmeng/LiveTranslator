import pytesseract
from pytesseract import Output

def extract_text_and_boxes(image, lang='eng', psm=6):
    """ Extract text by lines from an image using OCR. """
    config = f'--psm {psm} --oem 3 -l {lang}'
    data = pytesseract.image_to_data(image, config=config, output_type=Output.DICT)
    text_box_pairs = []
    current_block_num = None
    current_text = ''
    current_box = [0, 0, 0, 0]  # left, top, width, height

    for i in range(len(data['text'])):
        if data['text'][i].strip() != '':
            if data['block_num'][i] != current_block_num:
                if current_text:
                    text_box_pairs.append((current_text, tuple(current_box)))
                current_block_num = data['block_num'][i]
                current_text = data['text'][i]
                current_box = [data['left'][i], data['top'][i], data['width'][i], data['height'][i]]
            else:
                current_text += ' ' + data['text'][i]
                # Expand the bounding box to include this text
                current_box[2] = max(current_box[2], data['left'][i] + data['width'][i] - current_box[0])
                current_box[3] = max(current_box[3], data['top'][i] + data['height'][i] - current_box[1])

    if current_text:  # Add the last accumulated block
        text_box_pairs.append((current_text, tuple(current_box)))

    return text_box_pairs
