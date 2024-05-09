# import unittest
# from unittest.mock import patch

# from screen.FrameTranslator import FrameTranslator


# class TestFrameTranslator(unittest.TestCase):
#     @patch('screen.FrameTranslator.translate_text')
#     def test_frame_translator_worker(self, mock_translate_text):
#         mock_translate_text.return_value = "Translated"

#         translator = FrameTranslator(
#             'tests/sample.jpg', 'eng', 'fra', print_text=True, print_boxes=True)
#         translator.translation_queue.put(('Hello', (10, 10, 50, 20)))
#         translator.translation_queue.put(None)

#         translator.worker()

#         print("HELLO")

#         mock_translate_text.assert_called_once_with('Hello', 'fra')

#     @patch('screen.FrameTranslator.cv2.imshow')
#     @patch('screen.FrameTranslator.cv2.waitKey')
#     @patch('screen.FrameTranslator.cv2.destroyAllWindows')
#     def test_frame_translator_show_translated_frame(self, mock_destroyAllWindows, mock_waitKey, mock_imshow):
#         translator = FrameTranslator('tests/sample.jpg', 'eng', 'fra')
#         translator.show_translated_frame()

#         mock_imshow.assert_called_once()
#         mock_waitKey.assert_called_once()
#         mock_destroyAllWindows.assert_called_once()


# if __name__ == '__main__':
#     unittest.main()
