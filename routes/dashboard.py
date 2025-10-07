from flask import Blueprint, render_template, current_app
from routes.auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/", methods=["GET"])
@login_required
def dashboard():
    db = current_app.get_db()

    try:
        cur = db.execute("SELECT COUNT(*) FROM customers")
        num_of_customers = cur.fetchone()[0]        
        cur = db.execute("SELECT COUNT(*) FROM customers WHERE is_from_whatsapp = 1")
        num_of_customers_whatsapp = cur.fetchone()[0]        
        return render_template("dashboard.html", num_of_customers=num_of_customers, num_of_customers_whatsapp=num_of_customers_whatsapp)
    except Exception as e:
        print("Error", str(e))
        return render_template("dashboard.html", error=True)