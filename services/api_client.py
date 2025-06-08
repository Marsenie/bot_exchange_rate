import time
import aiohttp
from aiohttp import ClientError, ClientTimeout
from random import randint

class Client:
    def __init__(self, api_key_fixer: str, cache_ttl: int = 3000, timeout: int = 10):
        self.api_key_fixer = api_key_fixer
        self.base_url = "http://data.fixer.io/api"
        self.timeout = timeout  # Таймаут запроса в секундах

        self.cache: dict[str, tuple[float, dict]] = {}
        self.cache_ttl = cache_ttl  # Время жизни кэша в секундах

    async def get_course(self, code: str) -> dict:
        now = time.time()
        if code == "EUR":
            return 1.0
        
        # Проверка кэша
        if code in self.cache:
            ts, data = self.cache[code]
            if now - ts < self.cache_ttl:
                return data

        try:
            # Создаем клиент с таймаутом
            timeout = ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    async with session.get(
                        f"{self.base_url}/latest?access_key={self.api_key_fixer}"
                    ) as response:
                        data = await response.json()
                        if data["success"]:
                            # Сохраняем в кэш
                            self.cache[code] = (now, data["rates"][code])
                            return data["rates"][code]
                        else:
                            raise Exception(f"Failed to get data")
                        
                except ClientError as e:
                    # Обработка ошибок соединения/таймаута
                    raise Exception(f"Failed to get data: {str(e)}")
                    
        except Exception as e:
            # Обработка других исключений
            raise Exception(f"Unexpected error occurred: {str(e)}")
