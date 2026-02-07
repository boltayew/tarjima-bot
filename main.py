import telebot
from googletrans import Translator
import os

# Render uchun token (Buni keyinroq Render sozlamalariga qo'shamiz)
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
translator = Translator()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men 24/7 ishlovchi tarjimon botman. Menga matn yuboring, o'zbekchaga tarjima qilaman!")

@bot.message_handler(func=lambda message: True)
def translate_msg(message):
    try:
        # Kelgan matnni o'zbekchaga tarjima qilish
        res = translator.translate(message.text, dest='uz')
        bot.reply_to(message, res.text)
    except:
        bot.reply_to(message, "Kechirasiz, tarjimada xatolik bo'ldi.")

bot.infinity_polling()
