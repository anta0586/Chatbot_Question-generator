import os
import  telebot
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

model = "mistral-large-latest"
client = Mistral(api_key=api_key)

bot = telebot.TeleBot(token=telegram_token)

@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне текст, и я сгенерирую 5 вопросов по нему.")

def accept_message(message):
    return True

@bot.message_handler(func=accept_message)
def generate_questions(message):
    user_text = message.text

    if not user_text:
        bot.send_message(message.chat.id, "Ошибка: текст не должен быть пустым!")
        return

    bot.send_message(message.chat.id, "Генерирую вопросы... Подождите")

    try:
        # Отправляем запрос в Mistral AI для генерации ответа (из документации https://docs.mistral.ai/capabilities/completion/)
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"Твой ответ должен быть на языке запроса. Составь пять вопросов с вариантами ответов по следующему тексту: {user_text}"
                },
            ]
        )

            response_text = chat_response.choices[0].message.content

               bot.send_message(message.chat.id, response_text)

    except Exception as e:
      
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


bot.polling(none_stop=True)
