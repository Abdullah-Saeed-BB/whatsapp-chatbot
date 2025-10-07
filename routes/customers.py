from flask import Blueprint, request, current_app, Response, render_template
from datetime import date, timedelta
import random
import json

customers_bp = Blueprint("customers", __name__)

def generate_id():
    return "IRC" + str(random.random())[2:9]

@customers_bp.route("/", methods=["GET", "POST", "DELETE"])
def customers():
    db = current_app.get_db()
    try:
        if request.method == "GET":
            cur = db.execute("SELECT * FROM customers")
            customers = [dict(row) for row in cur.fetchall()]
            return render_template("customers.html", customers=customers)
            # return Response(json.dumps(rows), mimetype="application/json", status=200)
        elif request.method == "POST":
            # data = request.get_json()
            # id = generate_id()
            # match data.get("pay_style"):
            #     case "None": valid_until = date.today()
            #     case "monthly": valid_until = date.today() + timedelta(days=30)
            #     case "yearly": valid_until = date.today() + timedelta(days=365)
            #     case _:
            #         return Response(json.dumps({"error": "pay_style is incorrect or missing"}), mimetype="application/json", status=400)
            # valid_until = valid_until.isoformat()

            # db.execute("INSERT INTO customers (id, name, phone_num, plan, pay_style, valid_until, is_from_whatsapp) VALUES (?, ?, ?, ?, ?, ?, ?);",
            #            (id, data.get("name"), data.get("phone_num"), data.get("plan"), data.get("pay_style"), valid_until, data.get("is_from_whatsapp")))
            # db.commit()

            return Response(json.dumps({"message": "Customer subscription successed"}), mimetype="application/json")
        elif request.method == "DELETE":
            customer_id = request.args.get("id")

            if not customer_id:
                return Response(json.dumps({"error": "Missing id"}), mimetype="application/json", status=400)
            cur = db.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
            db.commit()
            if cur.rowcount == 0:
                return Response(json.dumps({"error": "Customer not found"}), mimetype="application/json", status=404)
            return Response(json.dumps({"message": "Subscription has been canceled"}), mimetype="application/json", status=200)
        
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), mimetype="application/json", status=500)
