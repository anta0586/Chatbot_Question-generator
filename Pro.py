# Необходимые импорты
import os
import  telebot
from mistralai import Mistral
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Загрузка модели Mistral AI
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

# Создание телеграм бота. В аргументе передается токен
bot = telebot.TeleBot(token=telegram_token)

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне текст, и я сгенерирую 5 вопросов по нему.")

def accept_message(message):
    return True

# Обработчик входящих текстовых сообщений
@bot.message_handler(func=accept_message)
def generate_questions(message):
    # Получаем текст сообщения и удаляем лишние пробелы
    user_text = message.text

    if not user_text:
        bot.send_message(message.chat.id, "Ошибка: текст не должен быть пустым!")
        return

    # Отправляем сообщение о генерации вопросов
    bot.send_message(message.chat.id, "Генерирую вопросы... Подождите")

    try:
        # Отправляем запрос в Mistral AI для генерации ответа (из документации https://docs.mistral.ai/capabilities/completion/)
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"Твой ответ должен быть на русском языке. Составь пять вопросов по следующему тексту: {user_text}"
                },
            ]
        )

        # Получаем текст сгенерированных вопросов
        response_text = chat_response.choices[0].message.content

        # Отправляем результат пользователю
        bot.send_message(message.chat.id, response_text)

    except Exception as e:
        # Ловим ошибку, если она произошла и сообщаем пользователю
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

# Запуск бота
bot.polling(none_stop=True)