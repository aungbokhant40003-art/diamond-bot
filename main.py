import telebot
import requests
import os
from flask import Flask
import threading

# --- BOT အချက်အလက်များ ---
# အစ်ကို့ရဲ့ Telegram Token
TG_TOKEN = '8482974569:AAES9ig4nWp0sFE5iHijuzxPsHqk4VKArzQ'
# အစ်ကို့ရဲ့ DeepSeek API Key
DEEPSEEK_KEY = 'd114f21983114da096fc69cc3f2fd300'

bot = telebot.TeleBot(TG_TOKEN)
app = Flask(__name__)

# --- Flask ပိုင်း (Render အခမဲ့ရအောင် Website အဖြစ် ဟန်ဆောင်ခြင်း) ---
@app.route('/')
def home():
    return "Aung Diamond Store Bot is Online!"

# --- DeepSeek AI နဲ့ ချိတ်ဆက်သည့်အပိုင်း ---
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
        ],
        "stream": False
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=20)
        res_json = response.json()
        return res_json['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return "ခေတ္တစောင့်ဆိုင်းပေးပါခင်ဗျာ။ စက်ပိုင်းဆိုင်ရာ အနည်းငယ် ပြင်ဆင်နေလို့ပါ။"

# --- Telegram မှ စာဝင်လာလျှင် ပြန်ဖြေသည့်အပိုင်း ---
@bot.message_handler(func=lambda m: True)
def reply_to_user(message):
    ai_response = ask_deepseek(message.text)
    bot.reply_to(message, ai_response)

# --- Bot ကို သီးသန့် အလုပ်လုပ်ခိုင်းခြင်း (Threading) ---
def run_bot():
    print("Telegram Bot is polling...")
    bot.infinity_polling()

if __name__ == "__main__":
    # Bot ကို Background မှာ Run ခိုင်းထားပါမည်
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Render အတွက် Port နံပါတ်ကို သတ်မှတ်ခြင်း
    # Render က ပေးတဲ့ Port ကို သုံးပါမယ်၊ မရှိရင် 10000 ကို သုံးပါမယ်
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
        
