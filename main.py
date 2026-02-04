import telebot
import requests
import os
from flask import Flask
import threading

# Bot အချက်အလက်
TG_TOKEN = '8482974569:AAES9ig4nWp0sFE5iHijuzxPsHqk4VKArzQ'
DEEPSEEK_KEY = 'd114f21983114da096fc69cc3f2fd300'

bot = telebot.TeleBot(TG_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def ask_deepseek(message_text):
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "သင်သည် Aung Diamond Store မှ အရောင်းဝန်ထမ်းဖြစ်သည်။ မြန်မာလို ယဉ်ကျေးစွာ ဖြေပါ။"},
            {"role": "user", "content": message_text}
        ]
    }
    try:
        res = requests.post(url, json=data, headers=headers, timeout=20).json()
        return res['choices'][0]['message']['content']
    except:
        return "ခေတ္တစောင့်ဆိုင်းပေးပါခင်ဗျာ။"

@bot.message_handler(func=lambda m: True)
def reply(m):
    bot.reply_to(m, ask_deepseek(m.text))

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Bot ကို သီးသန့် အလုပ်လုပ်ခိုင်းခြင်း
    threading.Thread(target=run_bot).start()
    # Render အတွက် Port ဖွင့်ပေးခြင်း
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
