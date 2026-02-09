import telebot
import sqlite3
from googletrans import Translator
from telebot import types

# --- SOZLAMALAR ---
TOKEN = '8525442823:AAHsrhnEMVOjMXteIJaiy--szLFLuU7JfHE'
ADMIN_ID = 7066979613

bot = telebot.TeleBot(TOKEN)
translator = Translator()

LANGUAGES_DICT = {
    'en': 'English', 'ru': 'Russian', 'uz': 'Uzbek', 'tr': 'Turkish',
    'de': 'German', 'fr': 'French', 'es': 'Spanish', 'it': 'Italian',
    'ko': 'Korean', 'ja': 'Japanese', 'zh-cn': 'Chinese'
}

# --- BAZA ---
def db_init():
    conn = sqlite3.connect('lingo_users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)')
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect('lingo_users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

db_init()

# --- ADMIN PANEL ---
@bot.message_handler(commands=['botusers'])
def get_stats(message):
    if message.from_user.id == ADMIN_ID:
        conn = sqlite3.connect('lingo_users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        conn.close()
        bot.send_message(ADMIN_ID, f"📊 *Bot foydalanuvchilari:* {count} ta", parse_mode='Markdown')

# --- INLINE MODE ---
@bot.inline_handler(lambda query: len(query.query) > 0)
def inline_translation(inline_query):
    try:
        add_user(inline_query.from_user.id)
        text = inline_query.query
        detection = translator.detect(text)
        detected_lang = detection.lang
        target = 'uz' if detected_lang != 'uz' else 'en'
        translated = translator.translate(text, dest=target)
        
        lang_full = LANGUAGES_DICT.get(detected_lang, detected_lang.upper())
        
        # Markdown formatini to'g'ri qo'llash
        result = types.InlineQueryResultArticle(
            id='1',
            title=f"Tarjima: {lang_full} -> {target.upper()}",
            description=translated.text,
            input_message_content=types.InputTextMessageContent(
                f"📝 *Matn:* {text}\n✅ *Tarjima:* {translated.text}",
                parse_mode='Markdown'
            )
        )
        bot.answer_inline_query(inline_query.id, [result])
    except:
        pass

# --- ASOSIY ---
@bot.message_handler(commands=['start'])
def welcome(message):
    add_user(message.from_user.id)
    bot.reply_to(message, "Salom! Men Lingo uz tarjimon botiman.\n\n"
                          "🔹 Matn yuboring - tarjima qilaman.\n"
                          "🔹 Inline rejimda ishlayman.")

@bot.message_handler(func=lambda m: True)
def main_translator(message):
    add_user(message.from_user.id)
    try:
        detection = translator.detect(message.text)
        detected_lang_code = detection.lang
        lang_name = LANGUAGES_DICT.get(detected_lang_code, detected_lang_code.upper())
        target_lang = 'uz' if detected_lang_code !=
