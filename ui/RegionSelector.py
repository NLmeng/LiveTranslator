import tkinter as tk
from tkinter import Canvas


class RegionSelector:
    def __init__(self, app):
        self.app = app

    def start_selection(self):
        self.app.root.withdraw()
        self.selection_window = tk.Toplevel(self.app.root)
        self.selection_window.attributes("-alpha", 0.3)
        self.selection_window.attributes("-topmost", True)
        self.selection_window.geometry(
            f"{self.app.root.winfo_screenwidth()}x{self.app.root.winfo_screenheight()}+0+0")

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
        self.app.capture_region = (self.selection_window.winfo_rootx() + min(self.start_x, self.end_x),
                                   self.selection_window.winfo_rooty() + min(self.start_y, self.end_y),
                                   abs(self.start_x - self.end_x),
                                   abs(self.start_y - self.end_y))
        self.selection_window.destroy()
        self.app.root.deiconify()
        self.app.window_combobox.config(state='normal')
