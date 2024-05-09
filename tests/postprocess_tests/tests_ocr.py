import unittest
from unittest.mock import ANY, patch

import cv2
import numpy as np
from pytesseract import Output

from screen.ocr import (extract_text_from_blocks, get_lang_charset,
                        segment_image)


class TestOCR(unittest.TestCase):

    def setUp(self):
        self.mock_image = np.zeros((500, 500, 3), np.uint8)

    @patch('pytesseract.image_to_data')
    def test_extract_text_from_blocks(self, mock_image_to_data):
        mock_data_1 = {
            'block_num': [1, 1, 1],
            'line_num': [1, 1, 2],
            'left': [0, 50, 0],
            'top': [0, 0, 50],
            'width': [50, 50, 100],
            'height': [50, 50, 50],
            'text': ['Hello', 'World']
        }

        mock_data_2 = {
            'block_num': [2, 2],
            'line_num': [1, 1],
            'left': [0, 50],
            'top': [0, 0],
            'width': [50, 100],
            'height': [50, 50],
            'text': ['Goodbye']
        }

        mock_image_to_data.side_effect = [mock_data_1, mock_data_2]
        bounding_boxes = [(0, 0, 100, 100), (0, 100, 100, 50)]
        extracted_texts = extract_text_from_blocks(
            self.mock_image, bounding_boxes, lang='eng')
        expected_texts = [('Hello World', (0, 0, 100, 50)),
                          ('Goodbye', (0, 100, 50, 50))]

        self.assertEqual(extracted_texts, expected_texts)
        mock_image_to_data.assert_any_call(
            ANY, config='--oem 3 -l eng', output_type=Output.DICT)

    @patch('cv2.cvtColor')
    @patch('cv2.adaptiveThreshold')
    @patch('cv2.getStructuringElement')
    @patch('cv2.dilate')
    @patch('cv2.findContours')
    def test_segment_image(self, mock_findContours, mock_dilate, mock_getStructuringElement, mock_adaptiveThreshold, mock_cvtColor):
        mock_cvtColor.return_value = np.ones((500, 500), np.uint8)
        mock_adaptiveThreshold.return_value = np.ones((500, 500), np.uint8)
        mock_kernel = np.ones((15, 5), np.uint8)
        mock_getStructuringElement.return_value = mock_kernel
        mock_dilate.return_value = np.ones((500, 500), np.uint8)

        mock_contours = [np.array([[10, 10], [10, 60], [60, 60], [60, 10]]), np.array(
            [[70, 70], [70, 120], [120, 120], [120, 70]])]
        mock_findContours.return_value = (mock_contours, None)

        bounding_boxes = segment_image(self.mock_image)

        expected_bounding_boxes = [(10, 10, 51, 51), (70, 70, 51, 51)]
        self.assertEqual(sorted(bounding_boxes),
                         sorted(expected_bounding_boxes))

        mock_cvtColor.assert_called_once_with(
            self.mock_image, cv2.COLOR_BGR2GRAY)
        mock_adaptiveThreshold.assert_called_once_with(
            ANY, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        mock_getStructuringElement.assert_called_once_with(
            cv2.MORPH_RECT, (15, 5))
        mock_dilate.assert_called_once_with(ANY, mock_kernel, iterations=2)
        mock_findContours.assert_called_once_with(
            ANY, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    def test_get_lang_charset(self):
        charset_eng = get_lang_charset('eng')
        charset_jpn = get_lang_charset('jpn')
        charset_fra = get_lang_charset('fra')
        charset_default = get_lang_charset('unknown')

        self.assertEqual(charset_eng, r'[a-zA-Z0-9\s,.!?;:-]')
        self.assertEqual(
            charset_jpn, r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\s,.!?;:-]')
        self.assertEqual(charset_fra, r'[a-zA-Z0-9\s,.!?;:\-àâçéèêëîïôûùüÿœ]')
        self.assertEqual(charset_default, r'[a-zA-Z0-9\s,.!?;:-]')


if __name__ == '__main__':
    unittest.main()
