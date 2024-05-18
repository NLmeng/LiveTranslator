import unittest
from unittest.mock import ANY, MagicMock, patch

import cv2
import numpy as np
from PIL import ImageDraw, ImageFont

from screen.Postprocessor import Postprocessor


class TestPostprocessor(unittest.TestCase):
    def setUp(self):
        self.postprocessor = Postprocessor()

    @patch('cv2.imread')
    @patch('cv2.cvtColor')
    def test_get_image_from_path(self, mock_cvtColor, mock_imread):
        mock_imread.return_value = np.zeros((100, 100, 3), np.uint8)
        mock_cvtColor.return_value = np.ones((100, 100, 3), np.uint8)

        image = self.postprocessor.get_image_from_path(
            'dummy/path/to/image.png')

        mock_imread.assert_called_once_with('dummy/path/to/image.png')
        mock_cvtColor.assert_called_once_with(
            mock_imread.return_value, cv2.COLOR_BGR2RGB)
        np.testing.assert_array_equal(image, np.ones((100, 100, 3), np.uint8))

    @patch('cv2.GaussianBlur')
    def test_blur_background(self, mock_GaussianBlur):
        mock_frame = np.zeros((100, 100, 3), np.uint8)
        mock_blurred_box = np.ones((10, 10, 3), np.uint8)
        mock_GaussianBlur.return_value = mock_blurred_box

        box = (10, 10, 10, 10)
        result = self.postprocessor.blur_background(mock_frame, box)

        mock_GaussianBlur.assert_called_once_with(
            ANY, (15, 15), cv2.BORDER_DEFAULT)
        np.testing.assert_array_equal(
            result[10:20, 10:20], np.ones((10, 10, 3), np.uint8))

    @patch('cv2.rectangle')
    @patch('PIL.ImageFont.truetype')
    @patch('PIL.ImageDraw.Draw')
    def test_put_text_on_frame(self, mock_Draw, mock_truetype, mock_cv2_rectangle):
        mock_frame = np.zeros((100, 100, 3), np.uint8)

        mock_font = MagicMock(spec=ImageFont.ImageFont)
        mock_truetype.return_value = mock_font

        mock_font.getbbox.side_effect = lambda text: (0, 0, 10 * len(text), 10)

        mock_draw_instance = MagicMock(spec=ImageDraw.ImageDraw)
        mock_Draw.return_value = mock_draw_instance

        box = (10, 10, 10, 10)

        self.postprocessor.put_text_on_frame(
            mock_frame, 'Test', box, draw_box=True)

        mock_draw_instance.text.assert_called()

        mock_cv2_rectangle.assert_called()

    def test_wrap_text(self):
        text = "This is a long text that needs to be wrapped"
        max_width = 50
        font = ImageFont.load_default()

        wrapped_text = self.postprocessor.wrap_text(text, max_width, font)

        expected_lines = ["This is a", "long text",
                          "that needs", "to be", "wrapped"]
        self.assertEqual(wrapped_text, expected_lines)

    @patch('cv2.rectangle')
    def test_draw_bounding_boxes(self, mock_rectangle):
        mock_image = np.zeros((100, 100, 3), np.uint8)
        bounding_boxes = [(10, 10, 20, 20), (30, 30, 40, 40)]

        result = self.postprocessor.draw_bounding_boxes(
            mock_image, bounding_boxes)

        self.assertEqual(mock_rectangle.call_count, 2)
        mock_rectangle.assert_any_call(
            mock_image, (10, 10), (30, 30), (0, 255, 0), 2)
        mock_rectangle.assert_any_call(
            mock_image, (30, 30), (70, 70), (0, 255, 0), 2)
        np.testing.assert_array_equal(result, mock_image)


if __name__ == '__main__':
    unittest.main()
