from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F
from services.api_client import Client
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from config.settings_fixer import fixer_config
from keyboards.builders import main_kb

router = Router()

mal_client = Client(fixer_config.api_key_fixer)


# Использование: /transfer <iso> <iso>
@router.message(Command("transfer"))
async def cmd_transfer(message: Message):
    try:
        parts = message.text.split(maxsplit=2)
        code_1, code_2 = parts[1].strip(), parts[2].strip()
    except:
        return await message.reply(f"Произошла ошибка.", reply_markup=main_kb)
    await transfer(code_1, code_2, message)
    
    

async def transfer(code_1, code_2, message: Message):
    if len(code_1) != 3 or len(code_2) != 3:
        return await message.reply("Код валюты написан с ошибкой\nФормат: /transfer RUB USD", reply_markup=main_kb)

    try:
        response_1 = await mal_client.get_course(code_1)
        response_2 = await mal_client.get_course(code_2)
        return await message.reply(f"Курс:\n1 {code_1} = {round(response_1/response_2, 2)} {code_2}\n\n1 {code_1} = {round(response_1, 2)} EUR\n1 {code_2} = {round(response_2, 2)} EUR", reply_markup=main_kb)
    except:
        return await message.reply(f"Произошла ошибка апи.", reply_markup=main_kb)
    
    
