from tkinter import *


class mainWindow:
    def __init__(self, master, window_name):
        self.master = master
        self.master.title(window_name)
        self.master.minsize(600, 600)
        
        self.test_text = "hi"
        self.main_frame = Frame(self.master, bg="white", height=600, width=600)
        self.main_frame.pack(fill="both", expand="yes")

        self.lower_label = Label(self.main_frame, bg="white", width=450, height=450, text=self.test_text)
        self.lower_label.pack(fill="both", expand="yes")

        self.test_btn = Button(self.lower_label, text="test", command=self.do_sth)
        self.test_btn.pack(pady=0, side="bottom")


    def do_sth(self):
        self.test_text = "clicked"
        self.rerender()
    
    def rerender(self):
        self.lower_label.config(text=self.test_text)


def startGUI(window_name, **kwargs):
    """
    """

    root = Tk()
    app = mainWindow(root, window_name)
    root.mainloop()
    return app