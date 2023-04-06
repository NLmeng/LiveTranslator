import sys
import os
import platform
from src.ocr.extractTexts import extractTexts
from ui.UI  import startGUI
from src.openai.main import generate_response
#
#
if __name__ == '__main__':
    # main()
    # app = startGUI("main window")
    print(generate_response("text-davinci-003", "hi, i am testing for a response!"))
        
