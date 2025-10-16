from flask import Blueprint, render_template, current_app, request, redirect, url_for
from datetime import date, timedelta
import random

def generate_id():
    return "IRC" + str(random.random())[2:9]

subscription_bp = Blueprint("subscription", __name__)

@subscription_bp.route("/", methods=["GET", "POST"])
def subscription():
    
    if request.method == "POST":
        try:
            db = current_app.get_db()
            cols = ["name", "phone_num", "plan", "pay_style", "is_from_whatsapp"]
            data = dict([(key, str(request.form.get(key))) for key in cols])
            data["is_from_whatsapp"] = True if data["is_from_whatsapp"] == "on" else False 

            print(data)

            id = generate_id()
            match data.get("pay_style"):
                case "None": valid_until = date.today()
                case "monthly": valid_until = date.today() + timedelta(days=30)
                case "yearly": valid_until = date.today() + timedelta(days=365)
            valid_until = valid_until.isoformat()

            db.execute("INSERT INTO customers (id, name, phone_num, plan, pay_style, valid_until, is_from_whatsapp) VALUES (?, ?, ?, ?, ?, ?, ?);",
                       (id, data.get("name"), data.get("phone_num"), data.get("plan"), data.get("pay_style"), valid_until, data.get("is_from_whatsapp")))
            db.commit()

            return redirect(url_for("subscription.subscription_status", subs_id=id))
        except Exception as e:
            print("ERROR:", str(e))
            return render_template("subscription.html", error="Unable to submit the subscription.")
    
    plan = request.args.get("plan")
    is_from_whatsapp = True if request.args.get("ifw") and request.args.get("ifw").startswith("1") else False

    return render_template("subscription.html", plan=plan, is_from_whatsapp=is_from_whatsapp)
    
@subscription_bp.route("/<string:subs_id>", methods=["GET", "PUT", "DELETE"])
def subscription_status(subs_id):
    db = current_app.get_db()

    try:
        cur = db.execute("SELECT * FROM customers WHERE id = ?", (subs_id,))
        customer = cur.fetchone()
        return render_template("subscription_status.html", customer=customer, subs_id=subs_id)
    except:
        render_template("subscription_status.html", customer=[])
    