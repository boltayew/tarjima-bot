import telebot
import sqlite3
from googletrans import Translator

# --- SOZLAMALAR ---
TOKEN = '8525442823:AAHsrhnEMVOjMXteIJaiy--szLFLuU7JfHE' 
ADMIN_ID = 7066979613
bot = telebot.TeleBot(TOKEN)
translator = Translator()

# --- BAZA ---
def db_init():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    conn.close()

def add_user(user_id, name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?, ?)', (user_id, name))
    conn.commit()
    conn.close()

db_init()

# --- 1. ADMIN BUYRUQLARI (Tepada bo'lishi shart!) ---

@bot.message_handler(commands=['users'])
def get_stats(message):
    if message.from_user.id == ADMIN_ID:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        conn.close()
        bot.send_message(ADMIN_ID, f"📊 **Bot foydalanuvchilari soni:** {count} ta", parse_mode='Markdown')

@bot.message_handler(commands=['send'])
def send_ads(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.send_message(ADMIN_ID, "Xabarni yozing:")
        bot.register_next_step_handler(msg, start_broadcasting)

def start_broadcasting(message):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()
    conn.close()
    for user in users:
        try: bot.copy_message(user[0], message.chat.id, message.message_id)
        except: continue
    bot.send_message(ADMIN_ID, "✅ Yuborildi.")

# --- 2. START BUYRUQ ---

@bot.message_handler(commands=['start'])
def welcome(message):
    name = message.from_user.first_name
    add_user(message.from_user.id, name)
    bot.reply_to(message, f"Salom, **{name}**! 👋\n\nMen tarjimon botman. Matn yuboring.", parse_mode='Markdown')

# --- 3. TARJIMON (Eng pastda bo'lishi shart!) ---

@bot.message_handler(func=lambda m: True)
def main_translator(message):
    add_user(message.from_user.id, message.from_user.first_name)
    try:
        detection = translator.detect(message.text)
        target = 'uz' if detection.lang != 'uz' else 'en'
        translated = translator.translate(message.text, dest=target)
        bot.reply_to(message, f"🔍 Asl tili: {detection.lang.upper()}\n📝 Tarjima: {translated.text}")
    except:
        bot.reply_to(message, "Xato.")

bot.polling(none_stop=True)
