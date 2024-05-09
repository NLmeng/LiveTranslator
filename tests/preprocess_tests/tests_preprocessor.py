import unittest
from unittest.mock import patch

import cv2
import numpy as np

from preprocess.Preprocessor import Preprocessor


class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        self.test_image = np.zeros(
            (500, 500, 3), np.uint8)  # a black square image
        self.jpn_image1 = cv2.imread("tests/pics/jgg1.jpg")
        self.jpn_image1_90 = cv2.imread("tests/pics/jgg1_90.jpg")

    @patch('pytesseract.image_to_osd')
    def test_full_mock_90_eng(self, mock_image_to_osd):
        mock_image_to_osd.return_value = "Rotate: 90\nScript: English"
        preprocessor = Preprocessor(self.test_image)
        lang_code = preprocessor.get_lang_code()
        self.assertEqual(lang_code, 'eng')
        self.assertEqual(preprocessor.should_deskew, True)
        self.assertEqual(preprocessor.script, 'English')
        self.assertEqual(preprocessor.angle, 90)

    @patch('pytesseract.image_to_osd')
    def test_full_mock_eng(self, mock_image_to_osd):
        mock_image_to_osd.return_value = "Rotate: 0\nScript: English"
        preprocessor = Preprocessor(self.test_image)
        lang_code = preprocessor.get_lang_code()
        self.assertEqual(lang_code, 'eng')
        self.assertEqual(preprocessor.should_deskew, False)
        self.assertEqual(preprocessor.script, 'English')
        self.assertEqual(preprocessor.angle, 0)

    @patch('pytesseract.image_to_osd')
    @patch('cv2.warpAffine')
    def test_deskew_90_degrees(self, mock_warpAffine, mock_image_to_osd):
        mock_image_to_osd.return_value = "Rotate: 90\nScript: English"
        mock_warpAffine.return_value = np.zeros((500, 500, 3), np.uint8)

        preprocessor = Preprocessor(self.test_image)
        deskewed_image = preprocessor.deskew()

        self.assertTrue(preprocessor.should_deskew)
        self.assertEqual(preprocessor.angle, 90)
        mock_warpAffine.assert_called_once()
        self.assertIsNotNone(deskewed_image)

    @patch('pytesseract.image_to_osd')
    @patch('cv2.warpAffine')
    def test_deskew_180_degrees(self, mock_warpAffine, mock_image_to_osd):
        mock_image_to_osd.return_value = "Rotate: 180\nScript: English"
        mock_warpAffine.return_value = np.zeros((500, 500, 3), np.uint8)

        preprocessor = Preprocessor(self.test_image)
        deskewed_image = preprocessor.deskew()

        self.assertTrue(preprocessor.should_deskew)
        self.assertEqual(preprocessor.angle, 180)
        mock_warpAffine.assert_called_once()
        self.assertIsNotNone(deskewed_image)

    @patch('pytesseract.image_to_osd')
    def test_add_border(self, mock_image_to_osd):
        mock_image_to_osd.return_value = "Rotate: 0\nScript: English"
        preprocessor = Preprocessor(self.test_image)

        bordered_image = preprocessor.add_border()

        self.assertEqual(
            bordered_image.shape[0], self.test_image.shape[0] + 20)
        self.assertEqual(
            bordered_image.shape[1], self.test_image.shape[1] + 20)

    @patch('pytesseract.image_to_osd')
    def test_remove_noise(self, mock_image_to_osd):
        mock_image_to_osd.return_value = "Rotate: 0\nScript: English"
        preprocessor = Preprocessor(self.test_image)

        noise_removed_image = preprocessor.remove_noise()
        self.assertIsNotNone(noise_removed_image)

    @patch('pytesseract.image_to_osd')
    @patch('cv2.warpAffine')
    def test_process_image_with_deskew(self, mock_warpAffine, mock_image_to_osd):
        mock_image_to_osd.return_value = "Rotate: 90\nScript: English"
        mock_warpAffine.return_value = np.zeros((520, 520, 3), np.uint8)

        preprocessor = Preprocessor(self.test_image)
        processed_image = preprocessor.process_image()

        self.assertTrue(preprocessor.should_deskew)
        self.assertEqual(preprocessor.angle, 90)
        mock_warpAffine.assert_called_once()
        self.assertIsNotNone(processed_image)

    @patch('pytesseract.image_to_osd')
    def test_process_image_without_deskew(self, mock_image_to_osd):
        mock_image_to_osd.return_value = "Rotate: 0\nScript: English"

        preprocessor = Preprocessor(self.test_image)
        processed_image = preprocessor.process_image()

        self.assertFalse(preprocessor.should_deskew)
        self.assertEqual(preprocessor.angle, 0)
        self.assertIsNotNone(processed_image)

    # 'real' Japanese tests
    def test_full_jpn_standard(self):
        preprocessor = Preprocessor(self.jpn_image1)
        lang_code = preprocessor.get_lang_code()
        self.assertEqual(lang_code, 'jpn')
        self.assertEqual(preprocessor.should_deskew, False)
        self.assertEqual(preprocessor.script, 'Japanese')
        self.assertEqual(preprocessor.angle, 0)

    def test_full_jpn_90_rotated(self):
        preprocessor = Preprocessor(self.jpn_image1_90)
        lang_code = preprocessor.get_lang_code()
        self.assertEqual(lang_code, 'jpn')
        self.assertEqual(preprocessor.should_deskew, True)
        self.assertEqual(preprocessor.script, 'Japanese')
        self.assertEqual(preprocessor.angle, 270)  # 360 - 90 (counter clock)


if __name__ == '__main__':
    unittest.main()
