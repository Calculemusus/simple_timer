from .en import translations as en_translations
from .zh import translations as zh_translations

def get_translations(lang_code):
    if lang_code == 'zh':
        return zh_translations
    return en_translations