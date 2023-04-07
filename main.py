import sys
import os
import platform
import threading
import queue
from src.ocr.extractTexts import extractTexts
from ui.UI import startGUI
from src.openai.main import generate_response
from src.clipboard.main import start_listening
from src.office.onenote import write_to_onenote
from src.office.token import acquire_token_func


# Create a queue to store the copied content
copied_content_queue = queue.Queue()

def start_listening_with_queue(copied_content_queue):
    """
    Calls start_listening() and puts the new copied content in the queue
    :param copied_content_queue: The queue to store the copied content
    :type copied_content_queue: queue.Queue
    """
    for copied_content in start_listening():
        copied_content_queue.put(copied_content)

def process_copied_content():
    """
    Processes the copied content in the queue by generating a prompt and potentially a response
    """
    while True:
        if not copied_content_queue.empty():
            prompt = copied_content_queue.get()
            response = generate_response("gpt-3.5-turbo", prompt)
            # print(f"Generated prompt: {prompt}")
            # print(f"Generated response: {response}")

if __name__ == "__main__":
    # Start the start_listening_with_queue function in a separate thread
    listener_thread = threading.Thread(target=start_listening_with_queue, args=(copied_content_queue,), daemon=True)
    listener_thread.start()

    # Run the process_copied_content function in the main thread
    process_copied_content()
