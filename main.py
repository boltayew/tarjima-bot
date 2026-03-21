import telebot
import sqlite3
from googletrans import Translator

# --- TOKEN VA ADMIN ID ---
TOKEN = '8525442823:AAHsrhnEMVOjMXteIJaiy--szLFLuU7JfHE' 
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
    # INSERT OR IGNORE - agar user ID allaqachon bo'lsa, xato bermaydi va qo'shmaydi
    cursor.execute('INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)', (user_id, name))
    conn.commit()
    conn.close()

db_init()

# --- 1. ADMIN BUYRUQLARI ---

@bot.message_handler(commands=['botusers', 'users'])
def get_stats(message):
    if message.from_user.id == ADMIN_ID:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        conn.close()
        bot.send_message(ADMIN_ID, f"📊 **Botning faol foydalanuvchilari:** {count} ta", parse_mode='Markdown')

@bot.message_handler(commands=['send'])
def send_ads(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.send_message(ADMIN_ID, "Reklama xabarini yuboring:")
        bot.register_next_step_handler(msg, start_broadcasting)

def start_broadcasting(message):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()
    conn.close()
    
    count = 0
    for user in users:
        try: 
            bot.copy_message(user[0], message.chat.id, message.message_id)
            count += 1
        except: continue
    bot.send_message(ADMIN_ID, f"✅ Xabar {count} ta foydalanuvchiga yuborildi.")

# --- 2. ASOSIY QISM (TARJIMON VA USERNI RO'YXATGA OLISH) ---

@bot.message_handler(func=lambda m: True)
def main_handler(message):
    # FOYDALANUVCHINI HAR QANDAY XABARDA BAZAGA TEKSHIRIB QO'SHISH
    # Bu eski userlarni ham "tutib olish" imkonini beradi
    add_user(message.from_user.id, message.from_user.first_name)

    # Agar xabar /start bo'lsa
    if message.text == "/start":
        bot.reply_to(message, f"Salom, {message.from_user.first_name}! Matn yuboring, men tarjima qilaman.")
        return

    # Tarjima qismi
    try:
        detection = translator.detect(message.text)
        target = 'uz' if detection.lang != 'uz' else 'en'
        translated = translator.translate(message.text, dest=target)
        bot.reply_to(message, f"📝 Tarjima: {translated.text}")
    except:
        bot.reply_to(message, "Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

# Botni ishga tushirish
print("Bot ishlamoqda...")
bot.polling(none_stop=True)
