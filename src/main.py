import numpy as np
import cv2 as cv
from PIL import ImageGrab
# import pyautogui
import sys
import os
import platform

# The os.chdir changes the current working directory to the specified directory. 
# The os.path.dirname returns the directory component of a file path.
# the os.path.abspath returns the absolute file path of a file.
# The __file__ variable is a built-in variable that holds the file path of the current script.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def list_window_names():
    window_names = []

    if sys.platform == "darwin":
        from AppKit import NSWorkspace
        workspace = NSWorkspace.sharedWorkspace()
        for window in workspace.runningApplications():
            # if window.isActive():
            window_names.append(window.localizedName())
    elif sys.platform == "win32":
        (active_app_name, windowTitle) = _getActiveInfo_Win32() 

    return window_names

print(list_window_names())

while(True):
    screenshot  = ImageGrab.grab()
    screenshot = np.array(screenshot)
    # BGR -> RGB
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)   

    cv.imshow("img", screenshot)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


