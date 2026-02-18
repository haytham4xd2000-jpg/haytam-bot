import telebot
import random
import json
import os

# 🔑 Put your new BotFather token here
TOKEN = "8517879791:AAG0cpkLrpArAJebmv1m7Ec00fHKLZhDnkY"
bot = telebot.TeleBot(TOKEN)

# File to save user data
DATA_FILE = "haytam_data.json"

# Load existing data or start empty
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        user_memory = json.load(f)
else:
    user_memory = {}

# ---------------- Moroccan bro replies ----------------
greetings = ["Salam a bro 😎 Haytam m3ak!", "Yo khoya 🔥 Haytam here!", "Wesh labas 😏"]
how_are_you = ["Labas 3lia 😌 kolchi mzyan!", "Dayr jaw 🤖✨", "Hamdullah always 💪"]
sad_replies = ["Aww khoya 😕 chno وقع؟ Ana m3ak.", "Mat9l9ch 💪 Haytam kayn.", "Dima kayn lfaraj 🙌"]
angry_replies = ["Calm down bro 😎 everything gets fixed.", "Chill a khoya, we solve it 💪", "Don’t stress 🔥 Haytam is here."]
happy_replies = ["Yesss 😎 glad to hear that!", "Awesome 🔥 keep smiling!", "Haytam happy for you 😏"]
football_replies = ["Messi wela Ronaldo? 👀⚽", "Football howa l7ayat 😎⚽", "Achmen club katcheجع؟ 🔥"]
jokes = ["3lach lbot ma kaymchich lmdrassa? 7it kay3raf kolchi 🤖😂", "Ana bot walakin 3andi style 😎", "Rah Haytam howa lboss 💪🔥"]
default_replies = ["Hmm 🤔 gol lia ktar a {name}... Haytam kaytsena 😎", "Tell me more bro 😏", "Interesting 🤖 continue a khoya!"]

# ---------------- Helper functions ----------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(user_memory, f)

def get_level(xp):
    return xp // 10 + 1

# ---------------- Commands ----------------
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

# ---------------- Main chat ----------------
@bot.message_handler(func=lambda message: True)
def chat(message):
    text = message.text.lower()
    chat_id = str(message.chat.id)

    if chat_id not in user_memory:
        user_memory[chat_id] = {"name": None, "xp": 0, "team": None}

    user = user_memory[chat_id]

    # Save name first
    if user["name"] is None:
        user["name"] = message.text
        save_data()
        bot.reply_to(message, f"Zwin 🔥 Mr7ba bik {message.text}!")
        return

    user["xp"] += 1
    save_data()
    level = get_level(user["xp"])
    name = user["name"]

    # Smart matching
    if any(word in text for word in ["hi", "hello", "salam", "yo"]):
        bot.reply_to(message, random.choice(greetings) + f" {name}!")
    elif any(word in text for word in ["how are you", "labas", "ça va"]):
        bot.reply_to(message, random.choice(how_are_you))
    elif any(word in text for word in ["sad", "bad", "upset", "unhappy"]):
        bot.reply_to(message, random.choice(sad_replies))
    elif any(word in text for word in ["happy", "good", "fine", "cool"]):
        bot.reply_to(message, random.choice(happy_replies))
    elif any(word in text for word in ["angry", "mad", "frustrated"]):
        bot.reply_to(message, random.choice(angry_replies))
    elif any(word in text for word in ["football", "messi", "ronaldo", "club"]):
        bot.reply_to(message, random.choice(football_replies))
    elif any(word in text for word in ["joke", "dk", "funny"]):
        bot.reply_to(message, random.choice(jokes))
    elif "team" in text:
        team_name = message.text.split("team")[-1].strip()
        user["team"] = team_name
        save_data()
        bot.reply_to(message, f"Wa zwin 🔥 {team_name} team dialek! Dima rba7 💪⚽")
    elif "level" in text:
        bot.reply_to(message, f"⭐ You're level {level} with {user['xp']} XP!")
    elif "bye" in text or "bslama" in text:
        bot.reply_to(message, f"Bslama {name} 👋 Matghibch 3lina!")
    else:
        bot.reply_to(message, random.choice(default_replies).format(name=name))

# ---------------- Start bot ----------------
print("Haytam v4 is running 🔥")
bot.infinity_polling()
