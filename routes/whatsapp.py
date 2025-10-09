from flask import Blueprint, request, Response, current_app
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from routes.utils import load_system_instruction, get_history, save_history
import json
import os
from pprint import pprint

load_dotenv()

whatsapp_bp = Blueprint("whatsapp", __name__)

# Set up the model
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = None

@whatsapp_bp.route("/", methods=["POST"])
def whatsapp_webhook():
    user_msg = request.form.get("Body")  # User's message
    sender = request.form.get("From")
    user_name = request.form.get("ProfileName")

    msg = f"| {user_name} ({sender}): {user_msg} |"
    print("-" * (len(msg) + 2))
    print(msg)
    print("-" * (len(msg) + 2))

    resp = MessagingResponse()

    try:
        res = generate_response(user_msg, sender, user_name)

        print("AI:", res)
    except Exception as e:
        print(e)
        res = "Sorry, there error occures while generate the response. Please try again later.\n\nالمعذرة, ولكن هنالك خطأ حدث اثناء إنشاء الرد. الرجاء المحاولة مرة اخرى لاحقاً"
    
    resp.message(res)

    return str(resp)
    # response = Response(json.dumps({"res": res, "history": history}))
    # return response


def generate_response(body, sender, user_name):
    contents = get_history(sender, body, user_name)

    if not model:
        load_model()

    model_res = model.generate_content(contents=contents, generation_config={
        "temperature": .15,
        "max_output_tokens": 600
    })

    print(contents)


    if model_res.candidates and model_res.candidates[0].content.parts:
        # save_history(sender, contents, model_res["text"])
        # return model_res["text"]
        save_history(sender, contents, model_res.text)
        return model_res.text
    raise Exception("Model didn't response")
    

def load_model():
    global model
    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=load_system_instruction())
