import telebot
from telebot import types
from bs4 import BeautifulSoup
from telegram_feature.config import TELEGRAM_TOKEN
import requests


def extract_section_content(section_id):
    url = "http://localhost:8888/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    section = soup.find(id=section_id)
    if section:
        paragraphs = section.find_all("p")
        formatted_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        return formatted_text
    else:
        return "Section not found."


section_to_button = {
    "mainSection": "🏠 Main",
    "docsSection": "📚 Documentation",
    "airflowSection": "🛠️ Airflow",
    "mlflowSection": "🤖 MLflow",
}

button_to_section = {v: k for k, v in section_to_button.items()}

telegram_bot = telebot.TeleBot(TELEGRAM_TOKEN)


@telegram_bot.message_handler(commands=["start"])
def send_welcome_message(message):
    custom_keyboard = types.ReplyKeyboardMarkup(row_width=2)
    for button_text in button_to_section.keys():
        custom_keyboard.add(types.KeyboardButton(button_text))
    telegram_bot.send_message(
        message.chat.id,
        "Привет! Я бот. Содержимое какой страницы желаете получить?",
        reply_markup=custom_keyboard,
    )


@telegram_bot.message_handler(func=lambda message: True)
def handle_button_click(message):
    if message.text in button_to_section:
        section_id = button_to_section[message.text]
        content = extract_section_content(section_id)
        telegram_bot.send_message(message.chat.id, content)


if __name__ == "__main__":
    telegram_bot.polling()
