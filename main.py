import telebot
import requests

# အစ်ကို့ဆီကရတဲ့ အချက်အလက်တွေကို အတိအကျ ထည့်ပေးထားပါတယ်
TG_TOKEN = '8482974569:AAES9ig4nWp0sFE5iHijuzxPsHqk4VKArzQ'
DEEPSEEK_KEY = 'd114f21983114da096fc69cc3f2fd300'

bot = telebot.TeleBot(TG_TOKEN)

def ask_deepseek(message_text):
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "သင်သည် Aung Diamond Store မှ ကျွမ်းကျင်သော အရောင်းဝန်ထမ်းဖြစ်သည်။ ဝယ်သူများကို မြန်မာလို ယဉ်ကျေးစွာ ပြန်ဖြေပေးပါ။"},
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
    ai_response = ask_deepseek(m.text)
    bot.reply_to(m, ai_response)

if __name__ == "__main__":
    bot.infinity_polling()
