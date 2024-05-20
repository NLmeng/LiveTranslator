# TODO: 1. add option to select source and target languages (DONE)
# TODO: 2. add option to select interval (DONE)
# TODO: 3. capture specific window instead of screen
# TODO: 4. add option to click and drag portion to capture
# TODO: 5. look into windowOS (ignore for now)
# TODO: tooltip, capturing indication, other indications
import sys
import tkinter as tk
from tkinter import ttk

import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
from PIL import Image, ImageTk

if sys.platform == "darwin":
    from Quartz import (CGWindowListCopyWindowInfo, kCGNullWindowID,
                        kCGWindowListOptionOnScreenOnly)

from screen.FrameTranslator import FrameTranslator


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Window Capture and Translation")

        self.selected_window = tk.StringVar()
        self.capture_mode = tk.StringVar(value='Capture in Intervals')

        self.label_mode = tk.Label(
            root, text="Select capture mode:")
        self.label_mode.pack(pady=10)

        self.mode_options = ['Capture in Intervals', 'Capture and Wait']
        self.mode_combobox = ttk.Combobox(
            root, textvariable=self.capture_mode, values=self.mode_options)
        self.mode_combobox.pack(pady=10)

        self.label_interval = tk.Label(
            root, text="Set capture interval (seconds):")
        self.label_interval.pack(pady=10)

        self.interval_var = tk.IntVar(value=5)
        self.interval_spinbox = ttk.Spinbox(
            root, from_=1, to=60, textvariable=self.interval_var)
        self.interval_spinbox.pack(pady=10)

        self.start_button = tk.Button(
            root, text="Start Capture", command=self.start_capture)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(
            root, text="Stop Capture", command=self.stop_capture)
        self.stop_button.pack(pady=10)

        self.capturing = False
        self.current_screenshot_windows = []

        self.label = tk.Label(root, text="Select a window to capture:")
        self.label.pack(pady=10)

        self.window_combobox = ttk.Combobox(
            root, textvariable=self.selected_window)
        self.window_combobox.pack(pady=10)

        self.refresh_button = tk.Button(
            root, text="Refresh Windows", command=self.refresh_window_list)
        self.refresh_button.pack(pady=10)

        self.source_lang = tk.StringVar()
        self.target_lang = tk.StringVar()

        self.lang_options = {'English': 'eng',
                             'Japanese': 'jpn', 'French': 'fra'}

        self.label_source_lang = tk.Label(root, text="Select source language:")
        self.label_source_lang.pack(pady=10)

        self.source_lang_combobox = ttk.Combobox(
            root, textvariable=self.source_lang, values=list(self.lang_options.keys()))
        self.source_lang_combobox.pack(pady=10)

        self.label_target_lang = tk.Label(root, text="Select target language:")
        self.label_target_lang.pack(pady=10)

        self.target_lang_combobox = ttk.Combobox(
            root, textvariable=self.target_lang, values=list(self.lang_options.keys()))
        self.target_lang_combobox.pack(pady=10)

        self.refresh_window_list()

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

    def refresh_window_list(self):
        self.window_list = self.get_window_list()
        self.window_combobox['values'] = self.window_list

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
        self.interval = self.interval_var.get()
        self.capturing = True
        self.capture_and_translate()

    def stop_capture(self):
        self.capturing = False
        self.close_all_screenshot_windows()

    def capture_and_translate(self):
        if not self.capturing:
            return

        window_title = self.selected_window.get()
        source_lang_code = self.lang_options.get(self.source_lang.get(), '')
        target_lang_code = self.lang_options.get(self.target_lang.get(), 'eng')

        window_info = self.find_window(window_title)

        if window_info:
            self.close_all_screenshot_windows()
            self.root.after(1, self.capture_and_translate_delayed,
                            window_info, source_lang_code, target_lang_code)
        else:
            print(f"Window '{window_title}' not found.")
            self.root.after(self.interval * 1000, self.capture_and_translate)

    def capture_and_translate_delayed(self, window_info, source_lang_code, target_lang_code):
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
            frame=frame, source_lang=source_lang_code, target_lang=target_lang_code, print_text=False, print_boxes=False)
        translator.start_translation_process()

        self.show_translated_frame(translator.frame)

        if self.capture_mode.get() == 'Capture in Intervals':
            self.root.after(self.interval * 1000, self.capture_and_translate)
        else:
            self.wait_for_close_and_capture_again()

    def close_all_screenshot_windows(self):
        for window in self.current_screenshot_windows:
            window.destroy()
        self.current_screenshot_windows.clear()

    def show_translated_frame(self, frame):
        window = tk.Toplevel(self.root)
        window.bind("<Escape>", lambda e: self.on_window_close(window))
        window.bind("<Button-1>", lambda e: self.on_window_close(window))

        cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)
        tk_image = ImageTk.PhotoImage(pil_image)

        label = tk.Label(window, image=tk_image)
        label.image = tk_image
        label.pack()

        self.current_screenshot_windows.append(window)

    def on_window_close(self, window):
        window.destroy()
        self.current_screenshot_windows.remove(window)
        if not self.capturing:
            return
        if self.capture_mode.get() == 'Capture and Wait':
            self.root.after(self.interval * 1000, self.capture_and_translate)

    def wait_for_close_and_capture_again(self):
        if self.capturing and not self.current_screenshot_windows:
            self.root.after(self.interval * 1000, self.capture_and_translate)
        else:
            self.root.after(100, self.wait_for_close_and_capture_again)


def start_gui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()
