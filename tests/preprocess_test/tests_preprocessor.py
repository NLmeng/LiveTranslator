import unittest
from unittest.mock import patch
import numpy as np
from preprocess.Preprocessor import Preprocessor

class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        self.test_image = np.zeros((500, 500, 3), np.uint8)

    @patch('pytesseract.image_to_osd')
    def test_get_lang_code(self, mock_image_to_osd):
        mock_image_to_osd.return_value = "Orientation in degrees: 0\nScript: Japanese"

        preprocessor = Preprocessor(self.test_image)
        lang_code = preprocessor.get_lang_code()

        self.assertEqual(lang_code, 'jpn')

    @patch('pytesseract.image_to_osd')
    def test_detect_orientation(self, mock_image_to_osd):
        mock_image_to_osd.return_value = "Orientation in degrees: 90\nScript: English"

        preprocessor = Preprocessor(self.test_image)
        angle = preprocessor.detect_orientation()

        self.assertEqual(angle, 90)
        self.assertTrue(preprocessor.should_deskew)

    def test_deskew(self):
        preprocessor = Preprocessor(self.test_image)
        preprocessor.should_deskew = True
        skewed_image = preprocessor.deskew()
        self.assertEqual(skewed_image.shape, self.test_image.shape)

if __name__ == '__main__':
    unittest.main()
