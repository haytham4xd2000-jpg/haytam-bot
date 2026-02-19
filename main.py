import telebot
import json
import os
import random
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# ---------------- CONFIG ----------------
TOKEN = "8517879791:AAG0cpkLrpArAJebmv1m7Ec00fHKLZhDnkY"  # From BotFather
bot = telebot.TeleBot(TOKEN)
DATA_FILE = "haytam_data.json"

# ---------------- LOAD DATA ----------------
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        user_memory = json.load(f)
else:
    user_memory = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(user_memory, f)

def get_level(xp):
    return xp // 10 + 1

# ---------------- LOAD HUGGING FACE MODEL ----------------
model_name = "TheBloke/MPT-7B-Chat-GGUF"  # Free chat model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

def get_ai_reply(name, text):
    prompt = f"You are Haytam, a friendly Moroccan teen chatbot. Talk like a Moroccan bro with short fun replies and emojis. User's name is {name}. Reply naturally to: {text}"
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        output = model.generate(**inputs, max_new_tokens=80)
        reply = tokenizer.decode(output[0], skip_special_tokens=True)
        return reply
    except:
        fallback = ["Hmm 🤔 I hear you, tell me more!", "Interesting 😏 keep talking!", "I hear you 🔥"]
        return random.choice(fallback)

# ---------------- COMMANDS ----------------
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = str(message.chat.id)
    if chat_id not in user_memory:
        user_memory[chat_id] = {"name": None, "xp":0, "team": None}
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

# ---------------- MAIN CHAT ----------------
@bot.message_handler(func=lambda message: True)
def chat(message):
    chat_id = str(message.chat.id)
    text = message.text.strip()
    if chat_id not in user_memory:
        user_memory[chat_id] = {"name": None, "xp":0, "team": None}
    user = user_memory[chat_id]

    if user["name"] is None:
        user["name"] = text
        save_data()
        bot.reply_to(message, f"Zwin 🔥 Mr7ba bik {text}!")
        return

    user["xp"] += 1
    save_data()
    reply = get_ai_reply(user["name"], text)
    bot.reply_to(message, reply)

# ---------------- START BOT ----------------
print("Haytam Free AI is running 🔥")
bot.infinity_polling()
