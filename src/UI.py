from tkinter import *


class mainWindow:
    def __init__(self):
        self.length = 0
        self.width  = 0
        # Create an instance of tkinter window
        self.win = Tk()
        # Define the geometry of the window
        self.win.geometry("700x500")

    def display(self, img):
        
        frame = Frame(self.win, width=600, height=400)
        frame.pack()
        frame.place(anchor='center', relx=0.5, rely=0.5)

        # Create a Label Widget to display the text or Image
        label = Label(frame, image = img)
        label.pack()

        self.win.mainloop()
