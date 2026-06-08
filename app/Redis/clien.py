import redis
from app.config import HOST, PORT

r = redis.Redis(host=HOST, port=PORT, decode_responses=True)

# print(r.ping())   #Для проверки соединения с Redis, возвращает True если соединение успешно установлено