from googletrans import Translator


def translate_text(text, dest_language='en'):
    """Translate the given text to the desired language."""
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text
