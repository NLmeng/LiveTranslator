from deep_translator import GoogleTranslator as DeepLTranslator
from translate.BaseTranslator import BaseTranslator


class DLTranslator(BaseTranslator):
    def __init__(self):
        self.translator = DeepLTranslator()
    
    def translate(self, text, dest_language='en'):
        return self.translator.translate(text, target=dest_language)
