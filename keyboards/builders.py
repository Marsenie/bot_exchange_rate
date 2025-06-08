from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
start_list_kb = [
        [KeyboardButton(text="/help")],
    ]
start_kb = ReplyKeyboardMarkup(keyboard=start_list_kb,
                               resize_keyboard=True,
                               one_time_keyboard=False)

main_list_kb = [
        [KeyboardButton(text="/favs")],
        [KeyboardButton(text="/support"), KeyboardButton(text="/help")],
    ]
main_kb = ReplyKeyboardMarkup(keyboard=main_list_kb,
                               resize_keyboard=True,
                               one_time_keyboard=False)
        
    

