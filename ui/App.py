import sys
import time
import tkinter as tk
from tkinter import ttk

import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
from PIL import Image, ImageGrab, ImageTk

if sys.platform == "darwin":
    from Quartz import (CGWindowListCopyWindowInfo, kCGNullWindowID,
                        kCGWindowListOptionOnScreenOnly, kCGWindowName)

from screen.FrameTranslator import FrameTranslator

# TODO: 1. add option to select source and target languages
# TODO: 2. add option to select interval
# TODO: 3. it seems to capture even the other window that is over the selected window
# TODO: 4. add option to click and drag to capture porion of the window (this one should behave like 3.)
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Window Capture and Translation")

        self.window_list = self.get_window_list()
        self.selected_window = tk.StringVar()

        self.label = tk.Label(root, text="Select a window to capture:")
        self.label.pack(pady=10)

        self.window_combobox = ttk.Combobox(
            root, textvariable=self.selected_window)
        self.window_combobox['values'] = self.window_list
        self.window_combobox.pack(pady=10)

        self.start_button = tk.Button(
            root, text="Start Capture", command=self.start_capture)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(
            root, text="Stop Capture", command=self.stop_capture)
        self.stop_button.pack(pady=10)

        self.interval = 5
        self.capturing = False

    def get_window_list(self):
        if sys.platform == "darwin":
            return self.get_window_list_macos()
        else:
            return self.get_window_list_windows()

    def get_window_list_macos(self):
        window_list = []
        options = kCGWindowListOptionOnScreenOnly
        window_info_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
        for window_info in window_info_list:
            window_name = window_info.get('kCGWindowName', 'Unknown')
            if window_name:
                window_list.append(window_name)
        return window_list

    def get_window_list_windows(self):
        windows = gw.getAllWindows()
        return [win.title for win in windows if win.isVisible]

    def find_window(self, title):
        if sys.platform == "darwin":
            options = kCGWindowListOptionOnScreenOnly
            window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
            for window in window_list:
                window_name = window.get('kCGWindowName', '')
                if window_name == title:
                    return window
        else:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                return windows[0]
        return None

    def start_capture(self):
        self.capturing = True
        self.capture_and_translate()

    def stop_capture(self):
        self.capturing = False

    def capture_and_translate(self):
        if not self.capturing:
            return

        window_title = self.selected_window.get()
        window_info = self.find_window(window_title)

        if window_info:
            if sys.platform == "darwin":
                bounds = window_info['kCGWindowBounds']
                x, y, width, height = map(
                    int, [bounds['X'], bounds['Y'], bounds['Width'], bounds['Height']])
            else:
                x, y, width, height = window_info.left, window_info.top, window_info.width, window_info.height

            img = pyautogui.screenshot(region=(x, y, width, height))
            np_img = np.array(img)
            frame = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)

            translator = FrameTranslator(
                frame=frame, print_text=False, print_boxes=False)
            translator.start_translation_process()

            self.show_translated_frame(translator.frame)
        else:
            print(f"Window '{window_title}' not found.")

        self.root.after(self.interval * 1000, self.capture_and_translate)

    def show_translated_frame(self, frame):
        window = tk.Toplevel(self.root)
        window.bind("<Escape>", lambda e: window.destroy())
        window.bind("<Button-1>", lambda e: window.destroy())

        cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)
        tk_image = ImageTk.PhotoImage(pil_image)

        label = tk.Label(window, image=tk_image)
        label.image = tk_image
        label.pack()


def start_gui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()
