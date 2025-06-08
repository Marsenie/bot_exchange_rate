from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from states.support_states import StatesSupport
from filters.filters import UserIsAdmin, MessageIsSupport
from config.settings_admins import admins_config
from config.settings_bot import bot_config

# Список администраторов
admins = admins_config.settings_admins
bot = Bot(token=bot_config.telegram_api_key)
router = Router()

# Обработчик команды /support для пользователей
@router.message(F.text == "/support")
async def start_support(message: types.Message, state: FSMContext):
    await state.set_state(StatesSupport.question)
    await message.answer("Опишите ваш вопрос или проблему. Мы ответим как только сможем.")

# Обработчик сообщения в состоянии ожидания вопроса
@router.message(StatesSupport.question)
async def process_question(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text, user_id=message.from_user.id)
    
    # Создаем клавиатуру для администраторов
    builder = InlineKeyboardBuilder()
    builder.button(text="Дать ответ", callback_data=f"reply_{message.from_user.id}")
    
    # Отправляем сообщение всем администраторам с обработкой ошибок
    for admin_id in admins:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=f"Вопрос от {message.from_user.full_name} (ID: {message.from_user.id}):\n\n"
                     f"{message.text}",
                reply_markup=builder.as_markup()
            )
        except Exception as e:
            print(f"Failed to send message to admin {admin_id}: {e}")
    
    await message.answer("Ваш вопрос отправлен в поддержку. Ожидайте ответа.")
    await state.clear()

# Обработчик ответов администраторов
@router.message(UserIsAdmin(), MessageIsSupport())
async def admin_reply(message: types.Message):
    original_message = message.reply_to_message.text
    user_id = int(original_message.split("ID: ")[1].split(")")[0])
    
    await bot.send_message(
        user_id,
        f"Ответ на ваш вопрос:\n\n{message.text}"
    )
    
    await message.answer("Ваш ответ отправлен.")

# Обработчик inline кнопки "Ответить"
@router.callback_query(F.data.startswith("reply_"))
async def process_reply_button(callback: types.CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split("_")[1])
    await state.update_data(target_user_id=user_id)
    await state.set_state(StatesSupport.response)
    await callback.message.answer(f"Напишите ответ для пользователя {user_id}:")
    await callback.answer()

# Обработчик ответа администратора в состоянии ожидания
@router.message(StatesSupport.response)
async def process_admin_response(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['target_user_id']
    
    await bot.send_message(
        user_id,
        f"Ответ поддержки:\n\n{message.text}"
    )
    
    await message.answer("Ответ отправлен.")
    await state.clear()


