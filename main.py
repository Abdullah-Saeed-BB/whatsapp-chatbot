from flask import Flask, g, render_template
import os
import sqlite3
from dotenv import load_dotenv
load_dotenv()

# Routes
from routes.customers import customers_bp
from routes.offers import offers_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp
from routes.chatbot_instruction import chatbot_instruction_bp
from routes.whatsapp import whatsapp_bp
from routes.subscription import subscription_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Change this to a random secret key

# Database
DATABASE = "db/creativecut.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

app.get_db = get_db
app.config["is_sys_instruction_updated"] = False

@app.route("/", methods=["GET"])
def home():
    return render_template("landing_page.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("not_found.html")

# register blueprints
app.register_blueprint(customers_bp, url_prefix="/api/customers")
app.register_blueprint(offers_bp, url_prefix="/api/offers")
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
app.register_blueprint(chatbot_instruction_bp, url_prefix="/api/chatbot_instruction")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(subscription_bp, url_prefix="/subscription")
app.register_blueprint(whatsapp_bp, url_prefix="/whatsapp")

if __name__ == "__main__":
    app.run(debug=True)
