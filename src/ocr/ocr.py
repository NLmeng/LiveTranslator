import numpy as np
import sys
import os
import cv2 as cv
import pygetwindow as gw
import Quartz
from PIL import ImageGrab, Image
from pytesseract import pytesseract
from deep_translator import GoogleTranslator

class OCR:
    def __init__(self):
        self.logfilename = "text_output.txt"
        self.change_working_directory()

    def change_working_directory(self):
        """
        The os.chdir changes the current working directory to the specified directory. 
        The os.path.dirname returns the directory component of a file path.
        the os.path.abspath returns the absolute file path of a file.
        The __file__ variable is a built-in variable that holds the file path of the current script.
        """
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        open(self.logfilename , "w").close()

    def choose_window(self):
        # List all open windows
        windows = []
        for window in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID):
            if window.get('kCGWindowOwnerName') and window.get('kCGWindowName'):
                windows.append(window)
        
        print("Available windows:")
        for i, window in enumerate(windows):
            print(f"{i + 1}. {window.get('kCGWindowOwnerName')} - {window.get('kCGWindowName')}")

        # Prompt the user to choose a window
        while True:
            try:
                choice = int(input("Enter the number of the window you want to capture: "))
                if 1 <= choice <= len(windows):
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        return windows[choice - 1]

    def screen_capture(self):
        #TODO: print message: "allow in Security & Privacy to enable" if not working / add to readme
        target_window = self.choose_window()
        if sys.platform == "darwin": 
            
            x, y, w, h = int(target_window['kCGWindowBounds']['X']), int(target_window['kCGWindowBounds']['Y']), int(target_window['kCGWindowBounds']['Width']), int(target_window['kCGWindowBounds']['Height'])
            screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            screenshot = np.array(screenshot)
            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
            self.extractTexts(screenshot)
            while True:
                cv.imshow("img", screenshot)

                if cv.waitKey(1) == ord('q'):
                    cv.destroyAllWindows()
                    break
        elif sys.platform == "win32":
        # TODO
            print()

    def extractTexts(self, img):  
        """
        use pytesseract
        processes (> greyscale > binary > dilute > contours) and extracts texts from img
        locate area of white pixels > draw boundary > crop > extract
        """
        greyed_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        bin0, bin1 = cv.threshold(
            greyed_img, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)
        dilation = cv.dilate(
            bin1,
            cv.getStructuringElement(cv.MORPH_RECT, (6, 6)),
            iterations=3
        )
        contours, hierarchy = cv.findContours(
            dilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        for curr in contours:
            x, y, w, h = cv.boundingRect(curr)

            cropped = img[y:y + h, x:x + w]
            text = pytesseract.image_to_string(cropped)
            translated_text = GoogleTranslator(source='auto', target='en').translate(text)

            file = open(self.logfilename , "w")
            file.write(translated_text + "\n")
            file.close

            # Draw translated text on the image
            img = cv.putText(img, translated_text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)