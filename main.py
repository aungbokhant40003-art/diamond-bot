import telebot
import requests
import os
from flask import Flask
import threading

# --- BOT အချက်အလက်များ ---
TG_TOKEN = '8482974569:AAES9ig4nWp0sFE5iHijuzxPsHqk4VKArzQ'
DEEPSEEK_KEY = 'sk-7050730862a9431199c1fe948530a4be'

bot = telebot.TeleBot(TG_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Aung Diamond Bot is Live!"

def ask_deepseek(message_text):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_KEY}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "သင်သည် Aung Diamond Store မှ အရောင်းဝန်ထမ်းဖြစ်သည်။ မြန်မာလို ယဉ်ကျေးစွာ ဖြေပါ။"},
            {"role": "user", "content": message_text}
        ]
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=20)
        return response.json()['choices'][0]['message']['content']
    except:
        return "ခေတ္တစောင့်ဆိုင်းပေးပါခင်ဗျာ။ စက်ပိုင်းဆိုင်ရာ ပြင်ဆင်နေလို့ပါ။"

@bot.message_handler(func=lambda m: True)
def reply(m):
    bot.reply_to(m, ask_deepseek(m.text))

if __name__ == "__main__":
    # Bot ကို Background မှာ Run ခိုင်းခြင်း
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    # Render Port ဖွင့်ခြင်း
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
