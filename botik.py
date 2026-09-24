import os
import telebot
from telebot import types
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN =8947714265:AAF-i4Oj-1kU2LRmgF6eq0SSiyPSag7JUOA
bot = telebot.TeleBot(TOKEN)

CHANNEL_USERNAME = "@MKINOHUB_HD"
CHANNEL_URL = "https://t.me/MKINOHUB_HD"

MOVIES = {
    "101": {
        "id": "ИНҶО_ФАЙЛ_АЙДИИ_ВИДЕОРО_МЕМОНИ", 
        "name": "Скуби-Ду"
    }
}

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

def is_subscribed(user_id):
    try:
        m = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return m.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking sub: {e}")
        return False

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):
        bot.send_message(message.chat.id, "👋 Хуш омадед ба KinoHUB!\n\n🎬 Коди филмро фиристед.")
    else:
        markup = types.InlineKeyboardMarkup()
        btn_sub = types.InlineKeyboardButton("📢 Подписаться на канал", url=CHANNEL_URL)
        btn_check = types.InlineKeyboardButton("✅ Проверить подписку", callback_data="check_sub")
        markup.add(btn_sub)
        markup.add(btn_check)
        bot.send_message(
            message.chat.id, 
            "⚠️ Барои истифодаи бот бояд ба канали мо обуна шавед!", 
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub_callback(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Подписка подтверждена!")
        bot.send_message(call.message.chat.id, "🎉 Ташаккур! Ҳоло коди филмро фиристед.")
    else:
        bot.answer_callback_query(call.id, "❌ Шумо ҳанӯз обуна нашудаед!", show_alert=True)

@bot.message_handler(content_types=['video'])
def get_file_id(message):
    file_id = message.video.file_id
    bot.send_message(message.chat.id, f"✅ File_id ин видео:\n\n`{file_id}`", parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def send_movie(message):
    if not is_subscribed(message.from_user.id):
        start_cmd(message)
        return
    code = message.text.strip()
    if code in MOVIES:
        bot.send_video(message.chat.id, MOVIES[code]["id"], caption=MOVIES[code]["name"])
    else:
        bot.send_message(message.chat.id, "❌ Филм бо ин код ёфт нашуд.")

if __name__ == "__main__":
    Thread(target=run_web_server, daemon=True).start()
    bot.infinity_polling()
    
