import telebot

# အစ်ကိုပေးတဲ့ Token ကို ထည့်ပေးထားပါတယ် [cite: 2026-02-07]
TOKEN = "8332511174:AAGAlFQk5SKWh5HSVakrzsrZYm424A7K9_w"
bot = telebot.TeleBot(TOKEN)

# "ဟိုင်း" ပို့ရင် "ဟလို" ပြန်မယ့်အပိုင်း [cite: 2026-02-06]
@bot.message_handler(func=lambda message: True)
def reply(message):
    if message.text == "ဟိုင်း":
        bot.reply_to(message, "ဟလို")
    else:
        bot.reply_to(message, "ဟိုင်း လို့ ပို့ကြည့်ပါဦးဗျ")

if __name__ == "__main__":
    bot.infinity_polling()
    
