# from google.genai.types import UserContent, ModelContent, Part
from flask import current_app, request
from cachetools import TTLCache
from twilio.rest import Client
import threading
import json
import os
import time
from dotenv import load_dotenv
load_dotenv()

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
twilio_whatsapp_num = os.getenv("TWILIO_WHATSAPP_NUM")

twilio_client = Client(account_sid, auth_token)

def get_subscription_details(subs_id, to_string=False):
    """
        Get all the details of the subscription. By providing the subscription id.
        Args:
            subscription_id: It starts by IRC then 7 random numbers 
    """
    db = current_app.get_db()    

    try:
        cur = db.execute("SELECT * FROM customers WHERE id = ?", (subs_id,))
        row = cur.fetchone()
        if not row: data = {"error": 404}
        else: data = dict(row)
    except:
        data = {"error": 400}

    if not to_string:
        return data

    match data.get("error"):
        case 404:
            return "Sorry, we didn't find a subscription with that ID. Please check the ID and try again\nنعتذر، لم نعثر على اشتراك بهذا ID. يُرجى التحقق من ID الصحيح والمحاولة مرة أخرى"
        case 400:
            return "Sorry, a technical issue occurred while retrieving your subscription data. Please try again later.\n نعتذر، حدثت مشكلة تقنية أثناء محاولة جلب بيانات اشتراكك. يُرجى المحاولة مرة أخرى في وقت لاحق."
        case _:
            try:
                return f"*ID:* {subs_id}\n*Name:* {data["name"]}\n*Phone Number:* {data["phone_num"]}\
                    \n*Plan:* {data["plan"]}\n*Pay Style:* {data["pay_style"]}\n*Valid Until:* {data["valid_until"]}\n\
                    \n*المعرف:* {subs_id}\n*الاسم:* {data["name"]}\n*رقم الجوال:* {data["phone_num"]}\
                    \n*خطة:* {data["plan"]}\n*اسلوب الدفع:* {data["pay_style"]}\n*تاريخ الانهاء:* {data["valid_until"]}"
            except: return data


def load_system_instruction():
    db = current_app.get_db()

    with open("./db/system_instruction.json") as f:
        sys = json.load(f)
    sys_txt = ""

    for key, value in sys.items():
        sys_txt += f"{key}:\n{value}\n\n"

    # Adding the offers in `system_instruction`
    sys_txt += "OFFERS:\n"
    cur = db.execute("SELECT * FROM offers")
    offers = cur.fetchall()
    if offers:
        for offer in offers:
            offer = dict(offer)
            sys_txt += f"{offer["title"]} - {offer["description"]}. Starts in {offer["valid_from"]} to {offer["valid_until"]}\n" 
    else:
        sys_txt += "There is no offer yet"

    return sys_txt

# For chats sessions
SESSION_CHAT_HISTORIES = TTLCache(maxsize=1000, ttl=600)

def get_history(user_id, new_message, user_name):
    if SESSION_CHAT_HISTORIES.get(user_id):
        print("FROM CHAT SESSION VARIABLE")
        new_contents = SESSION_CHAT_HISTORIES[user_id]
        new_contents.append({"role": "user", "parts": [f'{user_name}: {new_message}']})
 
    else:
        print("FROM TWILIO WHATSAPP API")
        try:
            inbound_messages = twilio_client.messages.list(from_=user_id, limit=2)

            outbound_messages = twilio_client.messages.list(to=user_id, limit=2)

            all_messages = inbound_messages + outbound_messages
            
            conversation = sorted(all_messages, 
                key=lambda m: m.date_sent or m.date_created # Sort by sent date, fallback to creation date
            )

            new_contents = list(map(lambda x: 
                        {"role": "user", "parts": [x.body]} if x.direction == "inbound"
                        else {"role": "model", "parts": [x.body]}, conversation))
            new_contents.append({"role": "user", "parts": [f'{user_name}: {new_message}']})
        except: 
            print("Error: Not able to load the converstion")
            new_contents = [{"role": "user", "parts": [f'{user_name}: {new_message}']}]

    return new_contents

def save_history(user_id, new_contents, new_model_res=None):
    if new_model_res:
        new_contents.append({"role": "model", "parts": new_model_res})
    SESSION_CHAT_HISTORIES[user_id] = new_contents

def background_cleanup():
    while True:
        list(SESSION_CHAT_HISTORIES.items()) 
        time.sleep(60)

cleanup_thread = threading.Thread(target=background_cleanup, daemon=True)
cleanup_thread.start()