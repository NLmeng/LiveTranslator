from deep_translator import GoogleTranslator


def translate(target_text, src_lang, target_lang):
    return GoogleTranslator(source=src_lang, target=target_lang).translate(target_text)
