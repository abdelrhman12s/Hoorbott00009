
import telebot
import requests

API_KEY = "AIzaSyDadpkfov7Wnd2NQj7UaW2bEAwQ87uqGhE"
BOT_TOKEN = "8186750168:AAF6GONeh2xZ7Tfex0d2YEVQVfU2FL-tUd0"
ADMIN_SECRET = "6666"
DEVELOPER_USERNAME = "@Abd0_technical"

bot = telebot.TeleBot(BOT_TOKEN)
user_histories = {}
admin_ids = set()

@bot.message_handler(commands=["start"])
def welcome(message):
    user = message.from_user.first_name
    bot.send_message(message.chat.id, f"أهلًا {user}، أنا بوت قصص مرعبة جداً!\nاضغط /story للحصول على قصة مرعبة\n\nللتواصل مع المطور: {DEVELOPER_USERNAME}")

@bot.message_handler(commands=["story"])
def generate_story(message):
    user_id = message.from_user.id
    prompt = "اكتب لي قصة مرعبة جدًا لا تصلح لأصحاب القلوب الضعيفة"
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}",
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    try:
        story = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        bot.send_message(message.chat.id, story)
        user_histories.setdefault(user_id, []).append(story)
    except Exception as e:
        bot.send_message(message.chat.id, "حدث خطأ أثناء توليد القصة، حاول مرة أخرى.")

@bot.message_handler(commands=["history"])
def get_history(message):
    uid = message.from_user.id
    history = user_histories.get(uid, [])
    if not history:
        bot.send_message(uid, "لا توجد قصص محفوظة لديك.")
    else:
        for i, s in enumerate(history[-5:], 1):
            bot.send_message(uid, f"📚 قصة #{i}:
{s}")

@bot.message_handler(commands=["admin"])
def admin_login(message):
    try:
        secret = message.text.split()[1]
        if secret == ADMIN_SECRET:
            admin_ids.add(message.from_user.id)
            bot.send_message(message.chat.id, "تم الدخول إلى لوحة الأدمن.")
        else:
            bot.send_message(message.chat.id, "رمز خاطئ.")
    except:
        bot.send_message(message.chat.id, "استخدم الأمر بهذا الشكل:\n/admin 6666")

@bot.message_handler(commands=["users"])
def user_count(message):
    if message.from_user.id in admin_ids:
        bot.send_message(message.chat.id, f"عدد المستخدمين: {len(user_histories)}")
    else:
        bot.send_message(message.chat.id, "أنت لست أدمن.")

print("البوت يعمل...")
bot.infinity_polling()
