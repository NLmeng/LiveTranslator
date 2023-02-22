import cv2 as cv
from pytesseract import pytesseract


#
# processes (> greyscale > binary > dilute > contours) and extracts texts from img
def extractTexts(img):  # use pytesseract
    greyed_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    bin0, bin1 = cv.threshold(
        greyed_img, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)
    # cv.imwrite('threshold_image.jpg',bin1)
    # print(pytesseract.image_to_string(bin1))
    dilation = cv.dilate(
        bin1,
        cv.getStructuringElement(cv.MORPH_RECT, (6, 6)),
        iterations=3
    )
    # cv.imwrite('dilation_image.jpg',dilation)
    contours, hierarchy = cv.findContours(
        dilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    # locate area of white pixels > draw boundary > crop > extract
    for curr in contours:
        x, y, w, h = cv.boundingRect(curr)

        cropped = img[y:y + h, x:x + w]
        text = pytesseract.image_to_string(cropped)

        file = open("text_output.txt", "a")
        file.write(text + "\n")
        file.close
