from datetime import datetime, timedelta
from aiogram import types
from aiogram import BaseMiddleware
from collections import defaultdict

class AntiSpamMW(BaseMiddleware):
    def __init__(self, limit=3, interval=5, ban_time=300):
        self.limit = limit
        self.interval = interval
        self.ban_time = ban_time  # Время бана в секундах
        self.user_data = defaultdict(dict)
        super().__init__()

    async def __call__(self, handler, message: types.Message, data: dict):
        user_id = message.from_user.id
        now = datetime.now()

        # Проверяем, не забанен ли пользователь
        if user_id in self.user_data and 'banned_until' in self.user_data[user_id]:
            if now < self.user_data[user_id]['banned_until']:
                return
            else:
                del self.user_data[user_id]['banned_until']

        # Инициализируем данные пользователя, если нужно
        if 'messages' not in self.user_data[user_id]:
            self.user_data[user_id]['messages'] = []

        # Очищаем старые сообщения
        self.user_data[user_id]['messages'] = [
            msg_time for msg_time in self.user_data[user_id]['messages'] 
            if (now - msg_time).seconds < self.interval
        ]

        # Проверяем лимит
        if len(self.user_data[user_id]['messages']) >= self.limit:
            self.user_data[user_id]['banned_until'] = now + timedelta(seconds=self.ban_time)

        # Добавляем текущее сообщение
        self.user_data[user_id]['messages'].append(now)
        
        return await handler(message, data)
