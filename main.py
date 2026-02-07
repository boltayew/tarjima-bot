import telebot
from googletrans import Translator
import os

# Bot tokeningizni o'zgaruvchidan oladi
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
translator = Translator()

# /start va /help buyruqlari
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Foydalanuvchining ismini olish (first_name)
    user_name = message.from_user.first_name
    welcome_text = (f"Salom {user_name}! 👋\n\n"
                    f"Menga istalgan tilda matn/so'z yuboring, "
                    f"men uni **O'zbek tiliga** tarjima qilaman. 🇺🇿")
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# Tarjima qilish qismi
@bot.message_handler(func=lambda message: True)
def translate_text(message):
    try:
        # Tilni aniqlash va tarjima qilish
        translation = translator.translate(message.text, dest='uz')
        
        # Asl tilning kodi (en, ru, tr va h.k.)
        source_lang_code = translation.src
        
        # Chiroyli javob matni
        response = (f"🔍 **Asl tili:** {source_lang_code.upper()}\n"
                    f"📝 **Tarjima:** {translation.text}")
        
        bot.reply_to(message, response, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, "❌ Xatolik yuz berdi. Matnni qayta yuborib ko'ring.")

# Render uchun portni sozlash
if __name__ == "__main__":
    from flask import Flask
    server = Flask(__name__)
    @server.route('/')
    def index(): return "Bot is running!"
    
    import threading
    threading.Thread(target=lambda: server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))).start()
    bot.infinity_polling()
