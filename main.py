import telebot
import json
import os
import openai

# ------------------- CONFIG -------------------
TOKEN = "8517879791:AAG0cpkLrpArAJebmv1m7Ec00fHKLZhDnkY"          # from BotFather
OPENAI_API_KEY = "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"  # get from https://platform.openai.com/account/api-keys

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

DATA_FILE = "haytam_data.json"

# ------------------- LOAD USER DATA -------------------
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        user_memory = json.load(f)
else:
    user_memory = {}

# ------------------- HELPER FUNCTIONS -------------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(user_memory, f)

def get_level(xp):
    return xp // 10 + 1

def get_ai_reply(user_name, text):
    prompt = f"""
You are a friendly Moroccan bro chatbot named Haytam.
You talk like a Moroccan teen, give short and fun replies, and sometimes use emojis.
The user’s name is {user_name}.
Respond naturally to this message: "{text}"
"""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=80
        )
        reply = response.choices[0].text.strip()
        return reply
    except Exception as e:
        return "Hmm 🤔 I can't think right now, but I got you later 😎"

# ------------------- COMMANDS -------------------
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = str(message.chat.id)
    if chat_id not in user_memory:
        user_memory[chat_id] = {"name": None, "xp": 0, "team": None}
        save_data()
    bot.reply_to(message, "Salam 😎 Ana Haytam! Shno smitek?")

@bot.message_handler(commands=['profile'])
def profile(message):
    chat_id = str(message.chat.id)
    user = user_memory.get(chat_id)
    if user:
        level = get_level(user["xp"])
        bot.reply_to(message,
            f"👤 Name: {user['name']}\n"
            f"⭐ XP: {user['xp']}\n"
            f"🏆 Level: {level}\n"
            f"⚽ Favorite Team: {user['team']}"
        )

@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
    leaderboard_list = sorted(user_memory.items(), key=lambda x: x[1]["xp"], reverse=True)[:10]
    text = "🏆 Haytam Leaderboard:\n\n"
    for i, (chat_id, user) in enumerate(leaderboard_list, start=1):
        level = get_level(user["xp"])
        name = user.get("name", "Unknown")
        text += f"{i}. {name} - Level {level} ({user['xp']} XP)\n"
    bot.reply_to(message, text)

# ------------------- MAIN CHAT -------------------
@bot.message_handler(func=lambda message: True)
def chat(message):
    chat_id = str(message.chat.id)
    text = message.text.strip()

    if chat_id not in user_memory:
        user_memory[chat_id] = {"name": None, "xp": 0, "team": None}

    user = user_memory[chat_id]

    # Save name first
    if user["name"] is None:
        user["name"] = text
        save_data()
        bot.reply_to(message, f"Zwin 🔥 Mr7ba bik {text}!")
        return

    # Increase XP
    user["xp"] += 1
    save_data()
    name = user["name"]

    # AI reply
    reply = get_ai_reply(name, text)
    bot.reply_to(message, reply)

# ------------------- START BOT -------------------
print("Haytam v5 AI is running 🔥")
bot.infinity_polling()
