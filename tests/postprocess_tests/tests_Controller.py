import unittest
from unittest.mock import MagicMock, patch

from screen.controller import get_image_from_path, put_text_on_frame


class TestController(unittest.TestCase):
    @patch('screen.controller.cv2.imread')
    @patch('screen.controller.cv2.cvtColor')
    def test_get_image_from_path(self, mock_cvtColor, mock_imread):
        mock_imread.return_value = MagicMock()
        mock_cvtColor.return_value = MagicMock()

        image = get_image_from_path('tests/sample.jpg')
        self.assertTrue(mock_imread.called)
        self.assertTrue(mock_cvtColor.called)
        self.assertIsNotNone(image)

    @patch('screen.controller.blur_background')
    @patch('screen.controller.cv2.putText')
    def test_put_text_on_frame(self, mock_putText, mock_blur_background):
        frame = MagicMock()
        text = 'Sample Text'
        box = (10, 10, 100, 20)

        put_text_on_frame(frame, text, box, draw_box=True)

        self.assertTrue(mock_blur_background.called)
        self.assertTrue(mock_putText.called)


if __name__ == '__main__':
    unittest.main()
