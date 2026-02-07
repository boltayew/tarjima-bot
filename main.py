import telebot
from deep_translator import GoogleTranslator
import os
from flask import Flask
from threading import Thread

# 1. Telegram Bot sozlamalari
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 2. Render uchun kichik Web Server (Bot o'chib qolmasligi uchun)
app = Flask('')

@app.route('/')
def home():
    return "Bot tirik!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 3. Bot funksiyalari
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men yana ishlayapman. Inglizcha matn yuboring.")

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    try:
        translated = GoogleTranslator(source='auto', target='uz').translate(message.text)
        bot.reply_to(message, translated)
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi.")

# 4. Ishga tushirish
if __name__ == "__main__":
    keep_alive()  # Web serverni yoqish
    bot.infinity_polling() # Botni yoqish
