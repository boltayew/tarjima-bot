import telebot
from googletrans import Translator

# TOKEN VA ADMIN ID
TOKEN = '8525442823:AAHsrhnEMVOjMXteIJaiy--szLFLuU7JfHE'
bot = telebot.TeleBot(TOKEN)
translator = Translator()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men tayyorman. Matn yuboring, tarjima qilaman.")

@bot.message_handler(func=lambda m: True)
def translate_text(message):
    try:
        # Avtomatik tilni aniqlash va tarjima qilish
        detection = translator.detect(message.text)
        dest_lang = 'uz' if detection.lang != 'uz' else 'en'
        translated = translator.translate(message.text, dest=dest_lang)
        
        # Oddiy matn formatisiz yuboramiz (xato bermasligi uchun)
        bot.reply_to(message, f"Tarjima ({dest_lang}):\n{translated.text}")
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi, qaytadan urinib ko'ring.")

bot.polling(none_stop=True)
