from flask import Blueprint, request, Response, render_template
from routes.auth import login_required
import json

chatbot_instruction_bp = Blueprint("chatbot_instruction", __name__)

@chatbot_instruction_bp.route("/", methods=["GET", "PUT"])
@login_required
def chatbot_instruction():
    try:
        with open("./db/system_instruction.json", "r") as f:
            data = json.load(f)
        if request.method == "GET":
            # return Response(json.dumps(data), mimetype="application/json", status=200)
            return render_template("chatbot_instruction.html", data=data)
        elif request.method == "PUT":
            new_data = request.get_json()
            new_keys = new_data.keys()

            for key in data.keys():
                if key in new_keys:
                    data[key] = new_data[key]
            
            with open("./db/system_instruction.json", "w") as f:
                json.dump(data, f, indent=4)

            return Response(json.dumps({"message": "System instruction updated"}))
        return Response(json.dumps({"error": "unvalid request method"}, status=403))

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), mimetype="application/json", status=500)
