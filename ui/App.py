import tkinter as tk
from tkinter import ttk

import cv2
import numpy as np
import pyautogui
from PIL import Image, ImageTk

from screen.FrameTranslator import FrameTranslator
from ui.RegionSelector import RegionSelector
from ui.ToolTip import ToolTip
from ui.WindowCapture import WindowCapture


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Window Capture and Translation")

        self.selected_window = tk.StringVar()
        self.capture_mode = tk.StringVar(value='Capture and Wait')
        self.capture_type = tk.StringVar(value='Region')

        self.label_mode = tk.Label(root, text="Select capture mode:")
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

        ToolTip(self.status_label, "Status of the running capture process.")

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

        self.capture_type_label = tk.Label(root, text="Select capture type:")
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

        self.window_capture = WindowCapture()
        self.region_selector = RegionSelector(self)

        self.capture_region = None
        self.refresh_window_list()

    def get_window_list(self):
        return self.window_capture.get_window_list()

    def refresh_window_list(self):
        self.window_list = self.get_window_list()
        self.window_combobox['values'] = self.window_list

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
        self.reset_ui_elements()

    def reset_ui_elements(self):
        self.selected_window.set("")
        self.capture_mode.set('Capture and Wait')
        self.capture_type.set('Region')
        self.interval_var.set(5)
        self.capture_region = None

        self.label_mode.pack(pady=10)
        self.mode_combobox.pack(pady=10)
        self.label_interval.pack(pady=10)
        self.interval_spinbox.pack(pady=10)
        self.start_button.pack(pady=10)
        self.stop_button.pack_forget()
        self.status_label.pack_forget()

        self.label_source_lang.pack(pady=10)
        self.source_lang_combobox.pack(pady=10)
        self.label_target_lang.pack(pady=10)
        self.target_lang_combobox.pack(pady=10)

        self.capture_type_label.pack(pady=10)
        self.capture_type_combobox.pack(pady=10)
        self.select_region_button.pack(pady=10)
        self.label.pack_forget()
        self.window_combobox.pack_forget()
        self.refresh_button.pack_forget()
        self.window_combobox.config(state='normal')

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

        window_info = self.window_capture.find_window(window_title)

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
        self.region_selector.start_selection()

    def capture_and_translate_delayed(self, window_info, source_lang_code, target_lang_code):
        x, y, width, height = self.window_capture.get_window_bounds(
            window_info)

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
