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
    except:
        return False

@bot.message_handler(commands=['start'])
def start_cmd(message):
    if is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "Хуш омадед! Коди филмро фиристед.")
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Обуна шудан", url=CHANNEL_URL))
        markup.add(types.InlineKeyboardButton("Санҷиши обуна ✅", callback_data="check"))
        bot.send_message(message.chat.id, "Аввал ба канал обуна шавед:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check_sub(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "Тасдиқ шуд!")
        bot.send_message(call.message.chat.id, "Ҳоло коди филмро фиристед.")
    else:
        bot.answer_callback_query(call.id, "Шумо ҳанӯз обуна нашудаед!", show_alert=True)

@bot.message_handler(content_types=['video'])
def get_file_id(message):
    bot.send_message(message.chat.id, f"File_id:\n`{message.video.file_id}`", parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def send_movie(message):
    if not is_subscribed(message.from_user.id):
        start_cmd(message)
        return
    code = message.text.strip()
    if code in MOVIES:
        bot.send_video(message.chat.id, MOVIES[code]["id"], caption=MOVIES[code]["name"])
    else:
        bot.send_message(message.chat.id, "Филм ёфт нашуд.")

if __name__ == "__main__":
    Thread(target=run_web_server, daemon=True).start()
    bot.infinity_polling()
  
