import threading
from queue import Queue

import cv2

from preprocess.Preprocessor import Preprocessor
from screen.controller import get_image_from_path, put_text_on_frame
from screen.ocr import extract_text_and_boxes
from translate.translator import translate_text


class FrameTranslator:
    def __init__(self, img_path, source_lang='', target_lang='eng', print_text=False, print_boxes=False):
        self.img_path = img_path
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.print_text = print_text
        self.print_boxes = print_boxes
        original_frame = get_image_from_path(img_path)
        preprocessor = Preprocessor(original_frame)
        if not source_lang or source_lang == '':
            source_lang = preprocessor.get_lang_code()
        self.frame = preprocessor.process_image()
        self.translation_queue = Queue()
        self.threads = []
        self.lang_code_map = {
            'eng': 'en',
            'jpn': 'ja',
            'fra': 'fr',
        }

    def worker(self):
        while True:
            item = self.translation_queue.get()
            if item is None:
                break
            text, box = item
            target_lang_code = self.lang_code_map.get(
                self.target_lang, self.target_lang)
            translated_text = translate_text(text, target_lang_code)
            put_text_on_frame(self.frame, translated_text,
                              box, draw_box=self.print_boxes)
            self.translation_queue.task_done()

    def start_translation_process(self):
        text_box_pairs = extract_text_and_boxes(self.frame, self.source_lang)

        for _ in range(4):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

        for text, box in text_box_pairs:
            if self.print_text:
                print(f"Text: {text}")
            self.translation_queue.put((text, box))

        for _ in range(4):
            self.translation_queue.put(None)

        for thread in self.threads:
            thread.join()

        cv2.imwrite("translated_frame.jpg", self.frame)
