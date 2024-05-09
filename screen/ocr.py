import re

import cv2
import pytesseract
from pytesseract import Output


def get_lang_charset(lang_code):
    """Returns a regular expression pattern for characters typical of the given language."""
    charsets = {
        'eng': r'[a-zA-Z0-9\s,.!?;:-]',
        'jpn': r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\s,.!?;:-]',  # Includes Kana and Kanji
        'fra': r'[a-zA-Z0-9\s,.!?;:\-àâçéèêëîïôûùüÿœ]',
    }
    return charsets.get(lang_code, r'[a-zA-Z0-9\s,.!?;:-]')

def extract_text_from_blocks(image, bounding_boxes, lang='eng'):
    """Extracts text from each block based on bounding boxes using pytesseract."""
    text_box_pairs = []
    language_pattern = get_lang_charset(lang)

    for box in bounding_boxes:
        x, y, w, h = box
        roi = image[y:y+h, x:x+w]
        data = pytesseract.image_to_data(roi, config=f'--oem 3 -l {lang}', output_type=Output.DICT)

        grouped_text = {}
        for i in range(len(data['text'])):
            if data['text'][i].strip() != '':
                filtered_text = ''.join(re.findall(language_pattern, data['text'][i]))
                if filtered_text:
                    key = (data['block_num'][i], data['line_num'][i])
                    left, top, width, height = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    box_in_roi = (left, top, width, height)
                    global_box = (x + box_in_roi[0], y + box_in_roi[1], box_in_roi[2], box_in_roi[3])

                    if key not in grouped_text:
                        grouped_text[key] = {'text': filtered_text, 'box': list(global_box)}
                    else:
                        grouped_text[key]['text'] += ' ' + filtered_text
                        grouped_text[key]['box'][2] = max(grouped_text[key]['box'][2], global_box[0] + global_box[2] - grouped_text[key]['box'][0])
                        grouped_text[key]['box'][3] = max(grouped_text[key]['box'][3], global_box[1] + global_box[3] - grouped_text[key]['box'][1])

        for key, value in grouped_text.items():
            text_box_pairs.append((value['text'], tuple(value['box'])))

    return text_box_pairs

def segment_image(image):
    """
        Segments the image into blocks of texts using contour detection.
        - applies grayscale
        - applies adaptive thresholding
        - dilates the image
        - finds contours
        - filters contours by size
        - sorts bounding boxes by y-coordinate
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 5))
    dilated = cv2.dilate(binary, kernel, iterations=2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = [cv2.boundingRect(contour) for contour in contours if cv2.contourArea(contour) > 500]

    bounding_boxes = sorted(bounding_boxes, key=lambda x: (x[1], x[0]))

    return bounding_boxes