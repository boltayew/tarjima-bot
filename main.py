import telebot
from googletrans import Translator
import os
from flask import Flask
import threading

# Sozlamalar
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
translator = Translator()
server = Flask(__name__)

@server.route('/')
def index():
    return "Bot is running!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (f"Salom {user_name}! 👋\n\n"
                    f"Menga istalgan tilda matn yuboring, "
                    f"men uni **O'zbek tiliga** tarjima qilaman. 🇺🇿")
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def translate_text(message):
    try:
        # Tilni avtomatik aniqlash va tarjima qilish
        translation = translator.translate(message.text, dest='uz')
        source_lang = translation.src.upper()
        
        response = (f"🔍 **Asl tili:** {source_lang}\n"
                    f"📝 **Tarjima:** {translation.text}")
        bot.reply_to(message, response, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, "❌ Tarjima qilishda xatolik yuz berdi.")

def run_server():
    port = int(os.environ.get('PORT', 8080))
    server.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Serverni alohida oqimda ishga tushirish
    threading.Thread(target=run_server).start()
    # Botni ishga tushirish
    bot.infinity_polling()
