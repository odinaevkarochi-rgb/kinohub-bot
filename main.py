import telebot
from telebot import types

# Токени боти ту
TOKEN = "7543818318:AAGoV26qGpxwR1ZpE0pC1O6mKk8eS2yv5m0"
bot = telebot.TeleBot(TOKEN)

# Канали ту барои обуна
CHANNEL_USERNAME = "@MKINOHUB_HD"
CHANNEL_URL = "https://t.me/MKINOHUB_HD"

# Базаи филмҳо (Код -> File ID-и филм)
MOVIES = {
    "101": "BAACAgIAAxkBAAM1Zv...1",  # Код ва File ID-и филмҳоро инҷо илова мекунӣ
}

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
            "🍿 **Добро пожаловать в KinoHUB!**\n\nОтправьте код фильма, чтобы получить его."
        )
    else:
        markup = types.InlineKeyboardMarkup()
        btn_sub = types.InlineKeyboardButton("Подписаться на канал 🍿", url=CHANNEL_URL)
        btn_check = types.InlineKeyboardButton("Проверить подписку 🔄", callback_data="check_sub")
        markup.add(btn_sub)
        markup.add(btn_check)
        bot.send_message(
            message.chat.id, 
            "⚠️ **Для использования бота необходимо подписаться на наш канал!**", 
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_callback(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Подписка подтверждена!")
        bot.send_message(call.message.chat.id, "🍿 Отправьте код фильма, чтобы получить его.")
    else:
        bot.answer_callback_query(call.id, "❌ Вы всё ещё не подписаны!", show_alert=True)

@bot.message_handler(func=lambda message: True)
def get_movie(message):
    user_id = message.from_user.id
    if not is_subscribed(user_id):
        start_cmd(message)
        return
    
    code = message.text.strip()
    if code in MOVIES:
        file_id = MOVIES[code]
        bot.send_video(message.chat.id, file_id, caption=f"🎬 Фильм по коду {code}\n\nПриятного просмотра от KinoHUB!")
    else:
        bot.send_message(message.chat.id, "❌ Фильм с таким кодом не найден. Проверьте код и попробуйте снова.")

if __name__ == "__main__":
    bot.infinity_polling()
      
