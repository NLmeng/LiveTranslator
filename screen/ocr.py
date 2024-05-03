import pytesseract
from pytesseract import Output


def extract_text_and_boxes(image, lang='eng', psm=6):
    """
        Use pytesseract's OCR.
        It groups text segments into blocks. Text within the same block is concatenated, and its bounding box is expanded to encompass new text segments.
        A complete text block is defined by a change in the block number or the end of the text list.
    """
    config = f'--psm {psm} --oem 3 -l {lang}'
    data = pytesseract.image_to_data(
        image, config=config, output_type=Output.DICT)
    text_box_pairs = []
    current_block_num = None
    current_text = ''
    current_box = [0, 0, 0, 0]

    for i in range(len(data['text'])):
        if data['text'][i].strip() != '':
            if data['block_num'][i] != current_block_num:
                if current_text:
                    text_box_pairs.append((current_text, tuple(current_box)))
                current_block_num = data['block_num'][i]
                current_text = data['text'][i]
                current_box = [data['left'][i], data['top']
                               [i], data['width'][i], data['height'][i]]
            else:
                current_text += ' ' + data['text'][i]
                current_box[2] = max(
                    current_box[2], data['left'][i] + data['width'][i] - current_box[0])
                current_box[3] = max(
                    current_box[3], data['top'][i] + data['height'][i] - current_box[1])

    if current_text:
        text_box_pairs.append((current_text, tuple(current_box)))

    return text_box_pairs
