import re

import pytesseract
from pytesseract import Output


def get_lang_charset(lang_code):
    """Returns a regular expression pattern for characters typical of the given language."""
    charsets = {
        'eng': r'[a-zA-Z0-9\s,.!?;:-]', # includes kana and kanji
        'jpn': r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\s,.!?;:-]',
        'fra': r'[a-zA-Z0-9\s,.!?;:\-àâçéèêëîïôûùüÿœ]',
    }
    return charsets.get(lang_code, r'[a-zA-Z0-9\s,.!?;:-]')


def extract_text_and_boxes(image, lang='eng', psm=6):
    config = f'--psm {psm} --oem 3 -l {lang}'
    data = pytesseract.image_to_data(
        image, config=config, output_type=Output.DICT)
    text_box_pairs = []
    current_block_num = None
    current_text = ''
    current_box = [0, 0, 0, 0]
    language_pattern = get_lang_charset(lang)

    for i in range(len(data['text'])):
        if data['text'][i].strip() != '':
            filtered_text = ''.join(re.findall(
                language_pattern, data['text'][i]))
            if filtered_text:
                if data['block_num'][i] != current_block_num:
                    if current_text:
                        text_box_pairs.append(
                            (current_text, tuple(current_box)))
                    current_block_num = data['block_num'][i]
                    current_text = filtered_text
                    current_box = [data['left'][i], data['top']
                                   [i], data['width'][i], data['height'][i]]
                else:
                    current_text += ' ' + filtered_text
                    current_box[2] = max(
                        current_box[2], data['left'][i] + data['width'][i] - current_box[0])
                    current_box[3] = max(
                        current_box[3], data['top'][i] + data['height'][i] - current_box[1])

    if current_text:
        text_box_pairs.append((current_text, tuple(current_box)))

    return text_box_pairs
