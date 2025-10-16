from flask import Blueprint, request, current_app
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from routes.utils import load_system_instruction, get_history, save_history, get_subscription_details
import re
import os

load_dotenv()

whatsapp_bp = Blueprint("whatsapp", __name__)

# Set up the model
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = None

@whatsapp_bp.route("/", methods=["POST"])
def whatsapp_webhook():
    user_msg = request.form.get("Body")
    sender = request.form.get("From")
    user_name = request.form.get("ProfileName")

    msg = f"| {user_name} ({sender}): {user_msg} |"
    print("-" * (len(msg)))
    print(msg)
    print("-" * (len(msg)))

    resp = MessagingResponse()

    try:
        res = generate_response(user_msg, sender, user_name)
    except Exception as e:
        print(e)
        res = "Sorry, there error occures while generate the response. Please try again later.\n\nالمعذرة, ولكن هنالك خطأ حدث اثناء إنشاء الرد. الرجاء المحاولة مرة اخرى لاحقاً"
    
    if type(res) == str:
        resp.message(res)
    else:
        print(res)
        resp.message(('\n-------\n'.join(res)))
        # for message in res:
        #     resp.message(message)

    return str(resp)

maximum_messages = 12

def generate_response(body, sender, user_name):
    contents = get_history(sender, body, user_name)
    messages_length = len(list(filter(lambda cont: cont["role"] == "model", contents)))

    print(f"HE GOT {maximum_messages - messages_length} MESSAGES LEFT")

    if messages_length > maximum_messages:
        return "Sorry, but you have reached the maximum messages. Try again later.\n\nالمعذرة, لقد وصلت الحد الأقصلا من الرسائل. حاول مرة اخرى لاحقاً."

    if not model or not current_app.config["is_sys_instruction_updated"]:
        load_model()
        current_app.config["is_sys_instruction_updated"] = True

    model_res = model.generate_content(contents=contents, generation_config={
        "temperature": .15,
        "max_output_tokens": 600
    })

    parts = model_res.candidates[0].content.parts

    messages = []

    try:
        if maximum_messages - messages_length <= 3:
            messages.append(
                f"You got {maximum_messages - messages_length} messages left\
                \nلديك فقد {maximum_messages - messages_length} رسائل متبقية",
            )
        if hasattr(parts[-1], "function_call") and parts[-1].function_call.name == "get_subscription_details":
            subs_id = parts[-1].function_call.args["subs_id"]
            subs_details = get_subscription_details(subs_id, to_string=True)
            if len(parts) > 1 and hasattr(parts[0], "text"):
                text = parts[0].text
                messages.append(clean_text(text))
            messages.append(subs_details)
        else:
            text = parts[0].text
            messages.append(clean_text(text))
    except Exception as e:
        print("Error while generate a response:", e)
        raise Exception("Model didn't response")

    save_history(sender, contents, messages[-1])
    return messages
    

def load_model():
    global model
    system_instruction = load_system_instruction()

    model = genai.GenerativeModel('gemini-2.5-flash',
                                  system_instruction=system_instruction,
                                  tools=[get_subscription_details])

def clean_text(txt):
    print("ORIGINAL TEXT:", txt)
    txt = " ".join(re.split(r"\[(\S+)\]\S+", txt))
    return txt