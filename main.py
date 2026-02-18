    import telebot
import openai
import json
import os

TOKEN = "8517879791:AAG0cpkLrpArAJebmv1m7Ec00fHKLZhDnkY"         # from BotFather
OPENAI_API_KEY = "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" # from OpenAI
bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

DATA_FILE = "haytam_data.json"

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

def get_ai_reply(name, text):
    try:
        prompt = f"""
You are Haytam, a friendly Moroccan teen chatbot.
Talk like a Moroccan bro with emojis and short fun replies.
User's name is {name}.
Reply naturally to: "{text}"
"""
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=80
        )
        reply = response.choices[0].text.strip()
        if reply == "":
            return "Hmm 🤔 I hear you, tell me more!"
        return reply
    except:
        return "Hmm 🤔 I can't think right now, but I'm here 😎"

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = str(message.chat.id)
    if chat_id not in user_memory:
        user_memory[chat_id] = {"name": None, "xp":0, "team": None}
        save_data()
    bot.reply_to(message, "Salam 😎 Ana Haytam! Shno smitek?")

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

print("Haytam AI is running 🔥")
bot.infinity_polling()
