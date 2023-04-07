import pyperclip
import time
import os

def start_listening():
    """
    Monitors the clipboard for changes, saves the new content to a file, and yields the new content
    :return: Yields the new content copied to the clipboard
    """
    # Initialize last_copied with the current content of the clipboard
    last_copied = pyperclip.paste()

    while True:
        current_copied = pyperclip.paste()
        
        if current_copied != last_copied:
            last_copied = current_copied
            # Save the new clipboard content to a file
            save_to_file(last_copied)
            # Yield the new clipboard content
            yield last_copied
        
        time.sleep(1)

def save_to_file(content):
    """
    Saves the given content to a file with a separator
    :param content: The content to be saved to the file
    :type content: str
    """
    with open("src/clipboard/clipboard_history.txt", "w") as f:
        f.write(f"{content}\n")
        f.write("===\n")
