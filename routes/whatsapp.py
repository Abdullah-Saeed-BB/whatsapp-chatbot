from flask import Blueprint, request, current_app
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from routes.utils import load_system_instruction, get_history, save_history
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
        for message in res:
            resp.message(message)

    return str(resp)

maximum_messages = 18

def generate_response(body, sender, user_name):
    contents = get_history(sender, body, user_name)

    if len(contents) > maximum_messages:
        return "Sorry, but you have reached the maximum messages. Try again later.\n\nالمعذرة, لقد وصلت الحد الأقصلا من الرسائل. حاول مرة اخرى لاحقاً."

    if not model or not current_app.config["is_sys_instruction_updated"]:
        load_model()
        current_app.config["is_sys_instruction_updated"] = True

    model_res = model.generate_content(contents=contents, generation_config={
        "temperature": .15,
        "max_output_tokens": 600
    })

    if model_res.candidates and model_res.candidates[0].content.parts:
        if len(contents) > maximum_messages - 2:
            return [
                model_res.text,
                f"You only got {maximum_messages - len(contents)} messages left\
                \nلديك فقد {maximum_messages - len(contents)} رسائل متبقية"
            ]

        save_history(sender, contents, model_res.text)
        return model_res.text
    raise Exception("Model didn't response")
    

def load_model():
    global model
    system_instruction = load_system_instruction()

    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)
