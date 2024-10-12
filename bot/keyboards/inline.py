from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardMarkup
from languages import languages

def start_kb(lang,key_1,key_2,key_3,key_4):
    txt_1 = languages[lang][key_1]
    txt_2 = languages[lang][key_2]
    txt_3 = languages[lang][key_3]
    txt_4 = languages[lang][key_4]
    start_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=txt_1, callback_data='zaqaz')],
        [
            InlineKeyboardButton(text=txt_2, callback_data='works'),
            InlineKeyboardButton(text=txt_3, callback_data='sahifa')
        ],
        [InlineKeyboardButton(text=txt_4,callback_data='change_lang')]
    ])
    return start_kb

def qayta_kb(lang,key_1,key_2):
    txt_1 = languages[lang][key_1]
    txt_2 = languages[lang][key_2]
    qayta_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=txt_1,callback_data='qayta_rest'),
        InlineKeyboardButton(text=txt_2,callback_data='qayta_break')]
    ])
    return qayta_kb


def last(lang,key_1,key_2):
    txt_1 = languages[lang][key_1]
    txt_2 = languages[lang][key_2]
    last_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=txt_1,callback_data='return')],
        [InlineKeyboardButton(text=txt_2,callback_data='zaqaz')]
    ])
    return last_kb

lang_keyb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data='lang_uz')],
    [InlineKeyboardButton(text="🇷🇺 Русский", callback_data='lang_ru')],
    [InlineKeyboardButton(text="🇬🇧 English", callback_data='lang_en')]
    ])

def stop(lang):
    txt = languages[lang]['stop'] 
    stop = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=txt,callback_data='break')]
    ])
    return stop


def are_you_sure(lang,key_1,key_2):
    txt_1 = languages[lang][key_1]
    txt_2 = languages[lang][key_2]
    are_you_sure = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=txt_1,callback_data='sure_yes'),InlineKeyboardButton(text=txt_2,callback_data='sure_no')]
    ])
    return are_you_sure

