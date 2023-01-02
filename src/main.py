import numpy as np
import cv2 as cv
from PIL import ImageGrab
import pygetwindow
import pyautogui
import sys
import os
import platform
#
#
def main():
    
    # The os.chdir changes the current working directory to the specified directory. 
    # The os.path.dirname returns the directory component of a file path.
    # the os.path.abspath returns the absolute file path of a file.
    # The __file__ variable is a built-in variable that holds the file path of the current script.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if sys.platform == "darwin": # allow in Security & Privacy to enable
        title = pygetwindow.getAllTitles()
        print(title)
        while(True):
            screenshot  = ImageGrab.grab(
                # all_screens=True,
                bbox=(0, 0, 200, 200),
                )
            screenshot = np.array(screenshot)
            # BGR -> RGB
            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)   

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
    main()

