
import sys
import tkinter as tk
from tkinter import Canvas, ttk

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
        self.capture_mode = tk.StringVar(value='Capture and Wait')
        self.capture_type = tk.StringVar(value='Region')

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
        self.stop_button.pack_forget()

        self.status_label = tk.Label(root, text="", wraplength=400)
        self.status_label.pack_forget()

        self.capturing = False
        self.current_screenshot_windows = []

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

        self.capture_type_label = tk.Label(
            root, text="Select capture type:")
        self.capture_type_label.pack(pady=10)

        self.capture_type_options = ['Window', 'Region']
        self.capture_type_combobox = ttk.Combobox(
            root, textvariable=self.capture_type, values=self.capture_type_options, state='readonly')
        self.capture_type_combobox.pack(pady=10)
        self.capture_type_combobox.bind(
            "<<ComboboxSelected>>", self.on_capture_type_change)

        self.label = tk.Label(root, text="Select a window to capture:")
        self.label.pack(pady=10)
        self.label.pack_forget()

        self.window_combobox = ttk.Combobox(
            root, textvariable=self.selected_window)
        self.window_combobox.pack(pady=10)
        self.window_combobox.pack_forget()

        self.refresh_button = tk.Button(
            root, text="Refresh Windows", command=self.refresh_window_list)
        self.refresh_button.pack(pady=10)
        self.refresh_button.pack_forget()

        self.select_region_button = tk.Button(
            root, text="Select Region", command=self.select_region)
        self.select_region_button.pack(pady=10)

        self.refresh_window_list()

        self.capture_region = None

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

    def on_capture_type_change(self, event):
        if self.capture_type.get() == 'Window':
            self.label.pack(pady=10)
            self.window_combobox.pack(pady=10)
            self.refresh_button.pack(pady=10)
            self.select_region_button.pack_forget()
        elif self.capture_type.get() == 'Region':
            self.label.pack_forget()
            self.window_combobox.pack_forget()
            self.refresh_button.pack_forget()
            self.select_region_button.pack(pady=10)

    def start_capture(self):
        self.interval = self.interval_var.get()
        self.capturing = True
        self.toggle_ui_elements(False)

        if self.capture_type.get() == 'Region':
            self.capture_selected_region()
        elif self.capture_type.get() == 'Window' and self.selected_window.get():
            self.capture_and_translate()
        else:
            print("No window or region selected for capture.")
            self.capturing = False
            self.toggle_ui_elements(True)

    def stop_capture(self):
        self.capturing = False
        self.close_all_screenshot_windows()
        self.toggle_ui_elements(True)

    def toggle_ui_elements(self, show):
        elements = [
            self.label_mode, self.mode_combobox, self.label_interval, self.interval_spinbox,
            self.start_button,
            self.label_source_lang, self.source_lang_combobox,
            self.label_target_lang, self.target_lang_combobox,
            self.capture_type_label, self.capture_type_combobox,
            self.select_region_button
        ]
        for element in elements:
            element.pack_forget() if not show else element.pack(pady=10)

        if show:
            self.stop_button.pack_forget()
            self.status_label.pack_forget()
        else:
            self.stop_button.pack(pady=10)
            self.status_label.config(
                text=f"Running with '{self.capture_mode.get()}' mode and '{self.capture_type.get()}' type...")
            self.status_label.pack(pady=10)

    def capture_selected_region(self):
        if not self.capturing:
            return

        def process_capture():
            x, y, width, height = self.capture_region

            img = pyautogui.screenshot(region=(x, y, width, height))
            np_img = np.array(img)
            frame = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)

            source_lang_code = self.lang_options.get(
                self.source_lang.get(), '')
            target_lang_code = self.lang_options.get(
                self.target_lang.get(), 'eng')

            translator = FrameTranslator(
                frame=frame, source_lang=source_lang_code, target_lang=target_lang_code, print_text=False, print_boxes=False)
            translator.start_translation_process()

            self.show_translated_frame(translator.frame)

            if self.capture_mode.get() == 'Capture in Intervals':
                self.root.after(self.interval * 1000,
                                self.capture_selected_region)
            else:
                self.wait_for_close_and_capture_region_again()

        self.close_all_screenshot_windows()
        self.root.after(1, process_capture)

    def wait_for_close_and_capture_region_again(self):
        if self.capturing:
            if not self.current_screenshot_windows:
                self.root.after(self.interval * 1000,
                                self.capture_selected_region)
            else:
                self.root.after(
                    100, self.wait_for_close_and_capture_region_again)

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

    def on_window_close(self, window):
        window.destroy()
        self.current_screenshot_windows.remove(window)
        if not self.capturing:
            return
        if self.capture_mode.get() == 'Capture and Wait':
            if self.capture_region:
                self.root.after(self.interval * 1000,
                                self.capture_selected_region)
            else:
                self.root.after(self.interval * 1000,
                                self.capture_and_translate)

    def select_region(self):
        self.selected_window.set("")
        self.window_combobox.config(state='disabled')
        self.root.withdraw()
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes("-alpha", 0.3)
        self.selection_window.attributes("-topmost", True)
        self.selection_window.geometry(
            f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")

        self.canvas = Canvas(self.selection_window, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.capture_region = (self.selection_window.winfo_rootx() + min(self.start_x, self.end_x),
                               self.selection_window.winfo_rooty() + min(self.start_y, self.end_y),
                               abs(self.start_x - self.end_x),
                               abs(self.start_y - self.end_y))
        self.selection_window.destroy()
        self.root.deiconify()
        self.window_combobox.config(state='disabled')

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

    def wait_for_close_and_capture_again(self):
        if self.capturing and not self.current_screenshot_windows:
            self.root.after(self.interval * 1000, self.capture_and_translate)
        else:
            self.root.after(1, self.wait_for_close_and_capture_again)


def start_gui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()
