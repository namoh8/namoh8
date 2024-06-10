import requests
import json
import random
import telebot
import time

ADD_MGM_DASHBOARD = "https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/info/apply"

bot = telebot.TeleBot("6911632621:AAEicC8lKzHcJ0WMOGhj1Z7JTnYs5pd62YM")

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, ''' مرحبا في بوت لوفي 🥷🏻😍
    يرجى إرسال رقم يوز لمواصلة العملية✅ ''')
    bot.register_next_step_handler(message, get_mobile_number)

def get_mobile_number(message):
    chat_id = message.chat.id
    mobile_number = message.text

    url = "https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "client_id": "ibiza-app",
        "grant_type": "password",
        "mobile-number": mobile_number,
        "language": "AR"
    }
    response = requests.post(url, headers=headers, data=payload)

    if "ROOGY" in response.text:
        otp = bot.send_message(chat_id, "OTP sent to your mobile. Please enter the OTP: ")
        bot.register_next_step_handler(otp, lambda message: verify_otp(message, chat_id, mobile_number, message.text))
    else:
        bot.send_message(chat_id, "Failed to send OTP. Please try again.")

def verify_otp(message, chat_id, mobile_number, otp):
    url = "https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "client_id": "ibiza-app",
        "grant_type": "password",
        "mobile-number": mobile_number,
        "language": "AR",
        "otp": otp
    }
    response = requests.post(url, headers=headers, data=payload)
    access_token = response.json().get("access_token")

    if access_token:
        apply_mgm_number(chat_id, access_token)
    else:
        bot.send_message(chat_id, "Failed to verify OTP.")

def apply_mgm_number(chat_id, access_token):
    invited_user_number = []

    for _ in range(8):
        invited_number = "05" + str(random.randint(1000000000, 9999999999))
        invited_user_number.append(invited_number)

    success_message_sent = False

    for number in invited_user_number:
        url = ADD_MGM_DASHBOARD

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "skipMgm": True,
            "mgmValue": "50",
            "referralCode": number
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            if response.status_code == 200 and not success_message_sent:
                response_json = response.json()
                show_won_popup = response_json.get("showWonPopUp", False)
                if show_won_popup:
                    bot.send_message(chat_id, '''تم  ارسال الانترنت بنجاح ✅ 
                    
                     @Dl_Luffy ''')
                else:
                    bot.send_message(chat_id, "Success! Invitation processed.")
                success_message_sent = True
            elif response.status_code != 200:
                bot.send_message(chat_id, '''❌لم تتم العملية بنجاح ، يرجى المحاولة بعد 2 دقائق🔁''' )

            time.sleep(2)

        except Exception as e:
            bot.send_message(chat_id, str(e))

if bot.polling : 
    print("bot started successful!✅")
else:
	print("bot not started! ❌")

bot.polling()
