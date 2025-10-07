from google.genai.types import UserContent, ModelContent, Part
from flask import current_app
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

key_words = ["status", "my biling", "my subscription"]
def is_check_billing_status(user_msg):
    pass

def get_biling_status(user_id):
    db = current_app.get_db()

    db.load 

def load_system_instruction(user_name):
    db = current_app.get_db()

    with open("./db/system_instruction.json") as f:
        sys = json.load(f)
    sys_txt = ""

    for key, value in sys.items():
        sys_txt += f"{key}:\n{value}\n\n"

    sys_txt += f"THE USER NAME IS: {user_name}\n\n" if user_name else ""

    # Adding the offers in `system_instruction`
    sys_txt += "OFFERS:\n"
    cur = db.execute("SELECT * FROM offers")
    for offer in cur.fetchall():
        offer = dict(offer)
        sys_txt += f"{offer["title"]} - {offer["description"]}. Starts in {offer["valid_from"]} to {offer["valid_until"]}\n" 

    return sys_txt

# For chats sessions
SESSION_CHAT_HISTORIES = TTLCache(maxsize=1000, ttl=300)

def get_history(user_id, new_message):
    if SESSION_CHAT_HISTORIES.get(user_id):
        new_contents = SESSION_CHAT_HISTORIES[user_id]
        new_contents.append(UserContent(parts=[Part(text=new_message)]))
 
    else:
        inbound_messages = twilio_client.messages.list(from_=user_id, limit=5)

        outbound_messages = twilio_client.messages.list(to=user_id, limit=5)

        all_messages = inbound_messages + outbound_messages
        
        conversation = sorted(all_messages, 
            key=lambda m: m.date_sent or m.date_created # Sort by sent date, fallback to creation date
        )

        

        new_contents = list(map(lambda x: 
                       UserContent(parts=[Part(text=x.body)]) if x.direction == "inbound"
                       else ModelContent(parts=[Part(text=x.body)]), conversation))
        new_contents.append(UserContent(parts=[Part(text=new_message)]))

    return new_contents

def save_history(user_id, new_contents, new_model_res=None):
    if new_model_res:
        new_contents.append(ModelContent(parts=[Part(text=new_model_res)]))
    SESSION_CHAT_HISTORIES[user_id] = new_contents

# def background_cleanup():
#     while True:
#         list(SESSION_CHAT_HISTORIES.items()) 
#         time.sleep(60)

# cleanup_thread = threading.Thread(target=background_cleanup, daemon=True)
# cleanup_thread.start()