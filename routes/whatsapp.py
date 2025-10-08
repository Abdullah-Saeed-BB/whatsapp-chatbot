from flask import Blueprint, request, Response, current_app
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from routes.utils import load_system_instruction, get_history, save_history
import json
import os

load_dotenv()

whatsapp_bp = Blueprint("whatsapp", __name__)

# Set up the model
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# model_client = genai.Client()
model = genai.GenerativeModel('gemini-2.5-flash')
# model = partial(model_client.models.generate_content, model="gemini-2.5-flash")


@whatsapp_bp.route("/", methods=["POST"])
def whatsapp_webhook():
    user_msg = request.form.get("Body")  # User's message
    sender = request.form.get("From")
    user_name = request.form.get("ProfileName")

    resp = MessagingResponse()

    try:
        res, hist = generate_response(user_msg, sender, user_name)
    except Exception as e:
        res = "Sorry, there error occures while generate the response. Please try again later.\n\nالمعذرة, ولكن هنالك خطأ حدث اثناء إنشاء الرد. الرجاء المحاولة مرة اخرى لاحقاً"
    
    resp.message(res)

    return Response(json.dumps({"resp": res, "history": list(map(lambda x: x.parts[0].text, hist))}), mimetype="application/json", status=200)

def generate_response(body, sender, user_name):
    system_instruction = load_system_instruction(user_name)

    contents = get_history(sender, body)

    model_res = model.generate_content(contents=contents, config=genai.types.GenerateContentConfig(
        temperature=.0,
        system_instruction=system_instruction,
        max_output_tokens=400
    ))

    save_history(sender, contents, model_res.text)

    return model_res.text, contents