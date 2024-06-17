from googletrans import Translator

from translate.BaseTranslator import BaseTranslator


class GoogleTranslator(BaseTranslator):
    def __init__(self):
        self.translator = Translator()

    def translate(self, text, dest_language='en'):
        translation = self.translator.translate(text, dest=dest_language)
        return translation.text
