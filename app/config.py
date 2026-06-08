import os
import dotenv

if os.path.exists(".env"):
    dotenv.load_dotenv(".env")
else:
    print("Файл .env не найден. Пожалуйста, создайте его и добавьте необходимые переменные окружения.")

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
