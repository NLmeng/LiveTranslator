import numpy as np
import cv2 as cv
from PIL import ImageGrab, Image
from pytesseract import pytesseract
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
    open("text_output.txt", "w").close()

    if sys.platform == "darwin": # allow in Security & Privacy to enable
        title = pygetwindow.getAllTitles()
        print(title)
        #
        while(True):
            #
            screenshot = ImageGrab.grab(
                # all_screens=True,
                bbox=(500, 0, 700, 500), #(left_x, top_y, right_x, bottom_y)
                )
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
# processes (> greyscale > binary > dilute > contours) and extracts texts from img
def extractTexts(img): # use pytesseract
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    bin0, bin1 = cv.threshold(gray_img, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)
    # cv.imwrite('threshold_image.jpg',bin1)
    # print(pytesseract.image_to_string(bin1))
    dilation = cv.dilate(
        bin1, 
        cv.getStructuringElement(cv.MORPH_RECT, (6, 6)), 
        iterations = 3
    )
    # cv.imwrite('dilation_image.jpg',dilation)
    contours, hierarchy = cv.findContours(dilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    # locate area of white pixels > draw boundary > crop > extract
    crop_number=0 
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        
        rect = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cropped = img[y:y + h, x:x + w]
        text = pytesseract.image_to_string(cropped)
    
        cv.imwrite("crop" + str(crop_number) + ".jpg", cropped)
        cv.imwrite('rectanglebox.jpg', rect)
        crop_number+=1
        file = open("text_output.txt", "a")
        file.write(text + "\n")
        file.close
#
#
if __name__ == '__main__':
    main()

