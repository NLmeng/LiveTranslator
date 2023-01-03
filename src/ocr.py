from deep_translator import GoogleTranslator
from pytesseract import pytesseract
import cv2 as cv

#
# processes (> greyscale > binary > dilute > contours) and extracts texts from img
def extractTexts(img): # use pytesseract
    greyed_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    bin0, bin1 = cv.threshold(greyed_img, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)
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
    for curr in contours:
        x, y, w, h = cv.boundingRect(curr)

        cropped = img[y:y + h, x:x + w]
        text = pytesseract.image_to_string(cropped)

        translated_text = translate(text, 'english', 'khmer')
        # rect = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv.imwrite("crop" + str(crop_number) + ".jpg", cropped)
        # cv.imwrite('rectanglebox.jpg', rect)
        crop_number+=1
        file = open("text_output.txt", "a")
        file.write(text + "  " + translated_text + "\n")
        file.close
#
#
def translate(target_text, src_lang, target_lang):
    return GoogleTranslator(source=src_lang, target=target_lang).translate(target_text)
        