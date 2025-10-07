from flask import Blueprint, request, current_app, Response, render_template, redirect, url_for
from routes.auth import login_required
import json

offers_bp = Blueprint("offers", __name__)

@offers_bp.route("/", methods=["GET", "POST"])
@login_required
def offers():
    db = current_app.get_db()
    try:
        if request.method == "GET":
            cur = db.execute("SELECT * FROM offers ORDER BY created_at DESC")
            rows = [dict(row) for row in cur.fetchall()]
            return render_template("offers.html", offers=rows)

        elif request.method == "POST":
            data = {
                "title": request.form.get("title"),
                "description": request.form.get("description"),
                "valid_from": request.form.get("valid_from"),
                "valid_until": request.form.get("valid_until")
            }
            db.execute(
                "INSERT INTO offers (title, description, valid_from, valid_until) VALUES (?, ?, ?, ?)",
                (data.get("title"), data.get("description"), data.get("valid_from"), data.get("valid_until"))
            )
            db.commit()
            # return Response(json.dumps({"message": "Offer created"}), mimetype="application/json", status=201)
            return redirect(url_for("offers.offers"))

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), mimetype="application/json", status=500)


@offers_bp.route("/api/<int:offer_id>", methods=["DELETE", "PUT"])
@login_required
def offers_api(offer_id):
    db = current_app.get_db()

    try:
        if request.method == "DELETE":
            if not offer_id:
                return Response(json.dumps({"error": "Missing id"}), mimetype="application/json", status=400)
            cur = db.execute("DELETE FROM offers WHERE id = ?", (offer_id,))
            db.commit()
            if cur.rowcount == 0:
                return Response(json.dumps({"error": "Offer not found"}), mimetype="application/json", status=404)
            return Response(json.dumps({"message": "Offer deleted"}), mimetype="application/json", status=200)
        elif request.method == "PUT":
            data = request.get_json()
            cur = db.execute(""" UPDATE offers 
                                SET title = ?, description = ?, valid_from = ?, valid_until = ?
                                WHERE id = ?;""", (data.get("title"), data.get("description"), data.get("valid_from"), data.get("valid_until"), offer_id))
            db.commit()
            if cur.rowcount == 0:
                return Response(json.dumps({"error": f"Offer not found for this id {offer_id}"}), mimetype="application/json", status=404)
            return Response(json.dumps({"message": "Offer updated"}), mimetype="application/json", status=200)
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), mimetype="application/json", status=500)
