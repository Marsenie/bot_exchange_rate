from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F
from services.favorites_storage import FavoritesStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from routers.exchange_rate import transfer, mal_client 
from keyboards.builders import main_kb

router = Router()

# инициализируем хранилище (файл рядом с bot.py: storage/favorites.json)
storage = FavoritesStorage("storage/favorites.json")

# ---- Добавить в избранное ----
# Использование: /add <iso> <iso>
@router.message(Command("add"))
async def cmd_add_fav(message: Message):
    parts = message.text.split(maxsplit=2)
    try:
        code_1, code_2 = parts[1].strip(), parts[2].strip()
    
        if len(code_1) != 3 or len(code_2) != 3:
            raise
    except:
        return await message.reply("Нужно написать коды валют: /add RUB USD", reply_markup=main_kb)

    await storage.add(message.from_user.id, f"{code_1} {code_2}")
    await message.reply(f"Отношению валют {code_1} {code_2} добавлено в избранное.", reply_markup=main_kb)

# ---- Список избранного ----
@router.message(Command("favs"))
async def cmd_list_fav(message: Message):
    favs = await storage.list(message.from_user.id)
    if not favs:
        return await message.reply("Пока нет избранного 🙁", reply_markup=main_kb)
    text = "Ваше избранное:\n" + "\n".join(f"- {a}" for a in favs)
    # кнопки для выбора каждого:
    kb = InlineKeyboardBuilder()
    for fav in favs:
        kb.button(text=f"Выбрать {fav}", callback_data=f"tranfer_currency {fav}")
    kb.adjust(1)
    await message.reply(text, reply_markup=kb.as_markup())

# Выбрать по кнопке
@router.callback_query(lambda c: c.data.startswith("tranfer_currency "))
async def cmd_tranfer_currency(query: CallbackQuery):
    parts = query.data.split(" ", 3)
    code_1, code_2 = parts[1].strip(), parts[2].strip()
    await transfer(code_1, code_2, query.message)

# ---- Удалить из избранного командой ----
@router.message(Command("del"))
async def cmd_remove_fav(message: Message):
    parts = message.text.split(maxsplit=2)
    try:
        code_1, code_2 = parts[1].strip(), parts[2].strip()
    
        if len(code_1) != 3 or len(code_2) != 3:
            raise
    except:
        return await message.reply("Нужно написать коды валют: /del RUB USD", reply_markup=main_kb)
    
    await storage.remove(message.from_user.id, f"{code_1} {code_2}")
    await message.reply(f"❌ Отношению валют {code_1} {code_2} удалено из избранного.", reply_markup=main_kb)



