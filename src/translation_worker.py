import threading
from queue import Queue

import cv2
import numpy as np

from screen.ocr import extract_text_and_boxes
from screen.preprocessor import cluster_text_boxes
from screen.screen_manipulator import capture_screenshot, put_text_on_frame
from translate.translator import translate_text


def worker(translation_queue, frame, print_boxes, target_lang):
    language_code_mapping = {
        'eng': 'en',  # English
        'jpn': 'ja',  # Japanese
        'fra': 'fr',  # French
    }

    while True:
        item = translation_queue.get()
        if item is None:
            break
        text, box = item
        target_lang_code = language_code_mapping.get(target_lang, target_lang)
        translated_text = translate_text(text, target_lang_code)
        put_text_on_frame(frame, translated_text, box, draw_box=print_boxes)
        translation_queue.task_done()


# TODO: use a clustering algorithm to group text_boxes
# then contcat them ensuring the order is correct (horizontally: going left-right -> top-bottom) (going pixels by pixels if necessary)
# TODO: fits the translated within the box
# TODO: deal with outliers, right now it seem there is one group of outlier that is grouped even though they are far
def start_translation_process(print_text=False, print_boxes=False, cluster_alg='dbscan', plot_clusters=False, source_lang='eng', target_lang='eng'):
    screenshot = capture_screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    text_box_pairs = extract_text_and_boxes(screenshot, lang=source_lang)
    clustered_text_box_pairs = cluster_text_boxes(text_box_pairs, cluster_alg, print_text, plot_clusters)

    translation_queue = Queue()
    threads = [threading.Thread(target=worker, args=(
        translation_queue, frame, print_boxes, target_lang)) for _ in range(4)]

    for thread in threads:
        thread.start()

    for text, box in clustered_text_box_pairs:
        translation_queue.put((text, box))

    for _ in range(4):
        translation_queue.put(None)

    for thread in threads:
        thread.join()

    cv2.imwrite("translated_frame.jpg", frame)
