import sys

if sys.platform == "darwin":
    from Quartz import (CGWindowListCopyWindowInfo, kCGNullWindowID,
                        kCGWindowListOptionOnScreenOnly)
else:
    import pygetwindow as gw


class WindowCapture:
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

    def get_window_bounds(self, window_info):
        if sys.platform == "darwin":
            bounds = window_info['kCGWindowBounds']
            x, y, width, height = map(
                int, [bounds['X'], bounds['Y'], bounds['Width'], bounds['Height']])
        else:
            x, y, width, height = window_info.left, window_info.top, window_info.width, window_info.height
        return x, y, width, height


# import time
# import tkinter as tk
# from subprocess import PIPE, Popen

# import cv2
# import numpy as np
# import pyautogui
# import pygetwindow as gw
# from PIL import Image, ImageTk, ImageGrab
# from Quartz import (CGWindowListCopyWindowInfo, kCGNullWindowID,
#                     kCGWindowListOptionOnScreenOnly, kCGWindowName)

# from screen.FrameTranslator import FrameTranslator

# def capture_screenshot(region=None):
#     """Capture a screenshot. If region is provided, captures a specific area."""
#     screen = ImageGrab.grab(bbox=region)
#     return screen

# def find_window(title):
#     """Use Quartz to find a window by title and return its geometry."""
#     options = kCGWindowListOptionOnScreenOnly
#     window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
#     for window in window_list:
#         window_name = window.get('kCGWindowName', '')
#         if window_name == title:
#             return window
#     return None


# def activate_window_with_applescript(title):
#     """Activate window using AppleScript (requires osascript)."""
#     script = f'''
#     tell application "System Events"
#         set myList to every process where visible is true
#         repeat with proc in myList
#             repeat with w in windows of proc
#                 if name of w contains "{title}" then
#                     set frontmost of proc to true
#                     return name of w -- Return the name for debugging
#                 end if
#             end repeat
#         end repeat
#         return "Window not found"
#     end tell
#     '''
#     p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE,
#               stderr=PIPE, universal_newlines=True)
#     stdout, stderr = p.communicate(script)
#     if stderr:
#         print("AppleScript error:", stderr)
#     print("AppleScript output:", stdout)
#     return stdout


# def capture_and_translate_window(window_title, interval=5, source_lang='eng', target_lang='eng', print_text=False, print_boxes=False, show=True):
#     try:
#         while True:
#             window_info = find_window(window_title)
#             if window_info:
#                 bounds = window_info['kCGWindowBounds']
#                 x, y, width, height = map(
#                     int, [bounds['X'], bounds['Y'], bounds['Width'], bounds['Height']])
#                 img = pyautogui.screenshot(region=(x, y, width, height))
#                 if img is None:
#                     print("Screenshot failed. Check region parameters.")
#                     continue
#                 np_img = np.array(img)
#                 try:
#                     frame = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
#                 except Exception as e:
#                     print("Error in converting image colors:", e)
#                     continue
#                 translator = FrameTranslator(
#                     frame=frame, source_lang=source_lang, target_lang=target_lang, print_text=print_text, print_boxes=print_boxes)
#                 translator.start_translation_process()
#                 if show:
#                     show_translated_frame(translator.frame)
#             else:
#                 print(f"Window '{window_title}' not found.")
#             time.sleep(interval)
#     except Exception as e:
#         print("Error capturing and translating window:", e)


# def show_translated_frame(frame):
#     """Display the translated frame in a tkinter window that closes on click or key press"""
#     window = tk.Tk()
#     window.bind("<Escape>", lambda e: window.quit())
#     window.bind("<Button-1>", lambda e: window.quit())
#     cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     pil_image = Image.fromarray(cv_image)
#     tk_image = ImageTk.PhotoImage(pil_image)
#     label = tk.Label(window, image=tk_image)
#     label.pack()
#     window.mainloop()


# def main(window_title, interval, source_lang, target_lang, print_text, print_boxes, show):
#     capture_and_translate_window(
#         window_title, interval, source_lang, target_lang, print_text, print_boxes, show)


# # TODO: windowsOS
# # def capture_and_translate_window(window_title, interval=5, target_lang='eng', show=True):
# #     try:
# #         while True:
# #             win = gw.getWindowsWithTitle(window_title)[0]
# #             if not win.isMinimized:
# #                 win.activate()
# #             img = pyautogui.screenshot(
# #                 region=(win.left, win.top, win.width, win.height))
# #             frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# #             translator = FrameTranslator(frame, target_lang=target_lang)
# #             translator.start_translation_process()

# #             if show:
# #                 show_translated_frame(translator.frame)

# #             time.sleep(interval)
# #     except Exception as e:
# #         print("Error capturing and translating window:", str(e))


# # def show_translated_frame(frame):
# #     """Display the translated frame in a tkinter window that closes on click or key press"""
# #     window = tk.Tk()
# #     window.bind("<Escape>", lambda e: window.quit())
# #     window.bind("<Button-1>", lambda e: window.quit())
# #     cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #     pil_image = Image.fromarray(cv_image)
# #     tk_image = ImageTk.PhotoImage(pil_image)
# #     label = tk.Label(window, image=tk_image)
# #     label.pack()
# #     window.mainloop()


# # def main(window_title, interval, target_lang, show):
# #     capture_and_translate_window(window_title, interval, target_lang, show)
