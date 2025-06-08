from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import logging
from keyboards.builders import main_kb, start_kb


router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я бот помогающий отслеживать курсы валют.\n"
                         "Введи /help для того, чтобы узнать мой функционал.",
                         reply_markup=start_kb)

    logging.info(f"User {message.from_user.id} called /start")

@router.message(Command("help"))
async def start_command(message: Message):
    await message.answer(
        "Команды:\n"
        "/start - Начало работы с ботом\n"
        "/transfer <iso> <iso> - выбрать город\n"
        "/favs - города в избранном\n"
        "/add <iso> <iso> - добавить город в избранное\n"
        "/del <iso> <iso> - удалить город в избранном\n"
        "/help- список команд\n"
        "/support- поддержка",
        reply_markup=main_kb
    )
