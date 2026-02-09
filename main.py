import telebot
import sqlite3
from googletrans import Translator

# --- SOZLAMALAR ---
TOKEN = '88525442823:AAHsrhnEMVOjMXteIJaiy--szLFLuU7JfHE' # Tokeningizni tekshirib oling
ADMIN_ID = 7066979613
bot = telebot.TeleBot(TOKEN)
translator = Translator()

# --- BAZA BILAN ISHLASH ---
def db_init():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    conn.close()

def add_user(user_id, name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)', (user_id, name))
    conn.commit()
    conn.close()

db_init()

# --- ADMIN BUYRUQLARI ---

# /users buyrug'i (avvalgi /botusers o'rniga)
@bot.message_handler(commands=['users'])
def get_stats(message):
    if message.from_user.id == ADMIN_ID:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        conn.close()
        bot.send_message(ADMIN_ID, f"📊 **Bot foydalanuvchilari soni:** {count} ta", parse_mode='Markdown')

# /send buyrug'i (Xabar tarqatish)
@bot.message_handler(commands=['send'])
def send_ads(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.send_message(ADMIN_ID, "Hamma foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing:")
        bot.register_next_step_handler(msg, start_broadcasting)

def start_broadcasting(message):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()
    conn.close()
    
    success = 0
    for user in users:
        try:
            bot.copy_message(user[0], message.chat.id, message.message_id)
            success += 1
        except:
            continue
    bot.send_message(ADMIN_ID, f"✅ Xabar {success} ta foydalanuvchiga yuborildi.")

# --- FOYDALANUVCHI UCHUN ---

@bot.message_handler(commands=['start'])
def welcome(message):
    name = message.from_user.first_name
    add_user(message.from_user.id, name)
    bot.reply_to(message, f"Salom, **{name}**! 😊\n\nMen aqlli tarjimon botman. Menga xohlagan tilda matn yuboring, men uni avtomatik aniqlab tarjima qilib beraman.", parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def main_translator(message):
    add_user(message.from_user.id, message.from_user.first_name)
    try:
        # Avtomatik tilni aniqlash
        detection = translator.detect(message.text)
        detected_lang = detection.lang
        
        # Agar yuborilgan matn o'zbekcha bo'lsa -> Inglizchaga, aks holda -> O'zbekchaga
        target = 'uz' if detected_lang != 'uz' else 'en'
        
        translated = translator.translate(message.text, dest=target)
        
        response = (f"🔍 **Aniqlangan til:** {detected_lang.upper()}\n"
                    f"📝 **Tarjima ({target.upper()}):**\n\n{translated.text}")
        
        bot.reply_to(message, response, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, "Tarjima qilishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

bot.polling(none_stop=True)
