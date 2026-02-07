import telebot
from deep_translator import GoogleTranslator
import os

# Tokenni Render-dagi Environment Variables-dan oladi
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men tarjimon botman. Menga inglizcha matn yuboring, men o'zbekchaga o'girib beraman.")

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    try:
        # Inglizchadan O'zbekchaga tarjima qilish
        translated = GoogleTranslator(source='auto', target='uz').translate(message.text)
        bot.reply_to(message, translated)
    except Exception as e:
        bot.reply_to(message, "Kechirasiz, tarjima qilishda xatolik yuz berdi.")

bot.infinity_polling()
