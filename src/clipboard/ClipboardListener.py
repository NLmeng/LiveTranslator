import pyperclip
import time
import os

class ClipboardListener:
    def __init__(self):
        self.last_copied = pyperclip.paste()

    def start_listening(self):
        """
        Monitors the clipboard for changes, saves the new content to a file, and yields the new content
        :return: Yields the new content copied to the clipboard
        """
        while True:
            current_copied = pyperclip.paste()

            if current_copied != self.last_copied:
                self.last_copied = current_copied
                # Save the new clipboard content to a file
                self.save_to_file(self.last_copied)
                # Yield the new clipboard content
                yield self.last_copied

            time.sleep(1)

    def save_to_file(self, content):
        """
        Saves the given content to a file with a separator
        :param content: The content to be saved to the file
        :type content: str
        """
        with open("src/clipboard/clipboard_history.txt", "w") as f:
            f.write(f"{content}\n")
            f.write("===\n")
