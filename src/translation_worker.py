import threading
from queue import Queue

import cv2
import numpy as np

from screen.ocr import extract_text_and_boxes
from screen.screen_manipulator import capture_screenshot, put_text_on_frame
from translate.translator import translate_text


def worker(translation_queue, frame):
    while True:
        item = translation_queue.get()
        if item is None:
            break
        text, box = item
        translated_text = translate_text(text)
        put_text_on_frame(frame, translated_text, box)
        translation_queue.task_done()


def start_translation_process():
    screenshot = capture_screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    text_box_pairs = extract_text_and_boxes(screenshot)

    translation_queue = Queue()
    threads = [threading.Thread(target=worker, args=(
        translation_queue, frame)) for _ in range(4)]

    for thread in threads:
        thread.start()

    for text, box in text_box_pairs:
        translation_queue.put((text, box))

    for _ in range(4):
        translation_queue.put(None)

    for thread in threads:
        thread.join()

    cv2.imwrite("translated_frame.jpg", frame)
