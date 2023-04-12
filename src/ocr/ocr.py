import numpy as np
import sys
import os
import cv2 as cv
from PIL import ImageGrab, Image
from pytesseract import pytesseract


class OCR:
    def __init__(self):
        self.change_working_directory()
        self.logfilename = "text_output.txt"

    def change_working_directory(self):
        """
        The os.chdir changes the current working directory to the specified directory. 
        The os.path.dirname returns the directory component of a file path.
        the os.path.abspath returns the absolute file path of a file.
        The __file__ variable is a built-in variable that holds the file path of the current script.
        """
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        open(self.logfilename , "w").close()

    def screen_capture(self):
        #TODO: print message: "allow in Security & Privacy to enable" if not working / add to readme
        if sys.platform == "darwin": 
            while True:
                screenshot = ImageGrab.grab()
                screenshot = np.array(screenshot)
                screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
                self.extractTexts(screenshot)
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

            file = open(self.logfilename , "w")
            file.write(text + "\n")
            file.close