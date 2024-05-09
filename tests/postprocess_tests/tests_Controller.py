import unittest
from unittest.mock import MagicMock, patch, ANY
import cv2
import numpy as np
from screen.controller import get_image_from_path, capture_screenshot, blur_background, put_text_on_frame, draw_bounding_boxes


class TestController(unittest.TestCase):
    @patch('cv2.imread')
    @patch('cv2.cvtColor')
    def test_get_image_from_path(self, mock_cvtColor, mock_imread):
        mock_imread.return_value = np.zeros((100, 100, 3), np.uint8)
        mock_cvtColor.return_value = np.ones((100, 100, 3), np.uint8)

        image = get_image_from_path('dummy/path/to/image.png')

        mock_imread.assert_called_once_with('dummy/path/to/image.png')
        mock_cvtColor.assert_called_once_with(mock_imread.return_value, cv2.COLOR_BGR2RGB)
        np.testing.assert_array_equal(image, np.ones((100, 100, 3), np.uint8))

    @patch('PIL.ImageGrab.grab')
    def test_capture_screenshot(self, mock_grab):
        mock_screenshot = MagicMock()
        mock_grab.return_value = mock_screenshot

        screen = capture_screenshot((0, 0, 100, 100))

        mock_grab.assert_called_once_with(bbox=(0, 0, 100, 100))
        self.assertEqual(screen, mock_screenshot)

    @patch('cv2.GaussianBlur')
    def test_blur_background(self, mock_GaussianBlur):
        mock_frame = np.zeros((100, 100, 3), np.uint8)
        mock_blurred_box = np.ones((10, 10, 3), np.uint8)
        mock_GaussianBlur.return_value = mock_blurred_box

        box = (10, 10, 10, 10)
        result = blur_background(mock_frame, box)

        mock_GaussianBlur.assert_called_once_with(ANY, (15, 15), cv2.BORDER_DEFAULT)
        np.testing.assert_array_equal(result[10:20, 10:20], np.ones((10, 10, 3), np.uint8))

    @patch('cv2.putText')
    @patch('cv2.rectangle')
    @patch('cv2.getTextSize')
    @patch('cv2.GaussianBlur')
    def test_put_text_on_frame(self, mock_GaussianBlur, mock_getTextSize, mock_rectangle, mock_putText):
        mock_frame = np.zeros((100, 100, 3), np.uint8)
        mock_blurred_box = np.ones((10, 10, 3), np.uint8)
        mock_GaussianBlur.return_value = mock_blurred_box
        mock_getTextSize.return_value = ((10, 10), 0)

        box = (10, 10, 10, 10)
        put_text_on_frame(mock_frame, 'Test', box, draw_box=True)

        mock_GaussianBlur.assert_called_once_with(ANY, (15, 15), cv2.BORDER_DEFAULT)
        mock_rectangle.assert_called_once_with(mock_frame, (10, 10), (20, 20), (0, 255, 0), 2)
        mock_putText.assert_called_once_with(mock_frame, 'Test', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    @patch('cv2.rectangle')
    def test_draw_bounding_boxes(self, mock_rectangle):
        mock_image = np.zeros((100, 100, 3), np.uint8)
        bounding_boxes = [(10, 10, 20, 20), (30, 30, 40, 40)]

        result = draw_bounding_boxes(mock_image, bounding_boxes)

        self.assertEqual(mock_rectangle.call_count, 2)
        mock_rectangle.assert_any_call(mock_image, (10, 10), (30, 30), (0, 255, 0), 2)
        mock_rectangle.assert_any_call(mock_image, (30, 30), (70, 70), (0, 255, 0), 2)
        np.testing.assert_array_equal(result, mock_image)


if __name__ == '__main__':
    unittest.main()
