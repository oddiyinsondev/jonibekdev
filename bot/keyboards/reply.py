from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder,ReplyKeyboardMarkup
from languages import languages

def phone_kb(lang,key):
    txt = languages[lang][key]
    phone_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=txt,request_contact=True)]
    ],
                                resize_keyboard=True,one_time_keyboard=True)
    return phone_kb


