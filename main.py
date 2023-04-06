import numpy as np
# import pygetwindow
# title = pygetwindow.getAllTitles()
# print(title)
import sys
import os
import platform
import cv2 as cv
from PIL import ImageGrab, Image
from src.ocr.extractTexts import extractTexts
from ui.UI  import startGUI
#
#
def main():
    # The os.chdir changes the current working directory to the specified directory. 
    # The os.path.dirname returns the directory component of a file path.
    # the os.path.abspath returns the absolute file path of a file.
    # The __file__ variable is a built-in variable that holds the file path of the current script.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    open("text_output.txt", "w").close()

    if sys.platform == "darwin": # allow in Security & Privacy to enable
        #
        while(True):
            #
            screenshot = ImageGrab.grab()
            screenshot = np.array(screenshot)
            # BGR -> RGB
            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
            #
            extractTexts(screenshot)
            #
            cv.imshow("img", screenshot)
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break
    # TODO
    elif sys.platform == "win32":
        print()
#
#
if __name__ == '__main__':
    # main()
    app = startGUI("main window")
        
