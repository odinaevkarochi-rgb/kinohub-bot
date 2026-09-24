import os
import telebot
from telebot import types
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = "8947714265:AAG-mO2sL6ZDAhjATJme1OtPaNYM7ObL3jo"
bot = telebot.TeleBot(TOKEN)

CHANNEL_USERNAME = "@MKINOHUB_HD"
CHANNEL_URL = "https://t.me/MKINOHUB_HD"

MOVIES = {
    "101": {
        "id": "BAACAgIAAxkBAAM...", 
        "name": "Скуби-Ду"
    }
}

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"KinoHUB Bot is alive and running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):
        bot.send_message(
            message.chat.id,
            "👋 Хуш омадед ба KinoHUB!\n\n🎬 Коди филмро фиристед ё /list-ро нависед.\n📥 Видеоро барои гирифтани file_id фиристед."
        )
    else:
        markup = types.InlineKeyboardMarkup()
        btn_sub = types.InlineKeyboardButton("Подписаться на канал 📢", url=CHANNEL_URL)
        btn_check = types.InlineKeyboardButton("Проверить подписку ✅", callback_data="check_sub")
        markup.add(btn_sub)
        markup.add(btn_check)
        bot.send_message(
            message.chat.id,
            "⚠️ Барои истифодаи бот лутфан ба канали мо обуна шавед!",
            reply_markup=markup
        )

@bot.message_handler(commands=['list'])
def list_movies(message):
    user_id = message.from_user.id
    if not is_subscribed(user_id):
        start_cmd(message)
        return
    
    text = "📋 Рӯйхати филмҳои мавҷуд:\n\n"
    for code, info in MOVIES.items():
        text += f" код `{code}` — {info['name']}\n"
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_callback(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Подписка подтверждена!")
        bot.send_message(call.message.chat.id, "🎉 Акнун метавонед кодҳоро фиристед.")
    else:
        bot.answer_callback_query(call.id, "❌ Шумо ҳанӯз обуна нашудаед!", show_alert=True)

@bot.message_handler(content_types=['video'])
def get_video_id(message):
    file_id = message.video.file_id
    bot.send_message(
        message.chat.id, 
        f"✅ File_id-и видео:\n\n`{file_id}`", 
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def get_movie(message):
    user_id = message.from_user.id
    if not is_subscribed(user_id):
        start_cmd(message)
        return

    code = message.text.strip()
    if code in MOVIES:
        file_id = MOVIES[code]["id"]
        bot.send_video(message.chat.id, file_id, caption="🎬 Приятного просмотра от KinoHUB!")
    else:
        bot.send_message(message.chat.id, "❌ Филм бо ин код ёфт нашуд. Барои гирифтани file_id видеоро фиристед.")

if __name__ == "__main__":
    t = Thread(target=run_web_server)
    t.daemon = True
    t.start()
    bot.infinity_polling()
      
