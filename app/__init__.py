from flask import Flask, render_template, request, redirect, url_for, flash, session
import socketio
import dotenv
from app.util.env import env
import paypalrestsdk
from app.util.animation import a

flask = Flask(__name__)
flask.config['SECRET_KEY']  = env("SECRET_KEY", "secret")
sio = socketio.Client()

jobs = {}

paypalrestsdk.configure({
    "mode": "sandbox" if env("ENVIRONMENT", "prod") == "dev" else "live",
    "client_id": env("PAYPAL_CLIENT_ID", "cid"),
    "client_secret": env("PAYPAL_CLIENT_SECRET", "pcs")
})

# Let's add a before_request handler
@flask.before_request
def before_request():
    if "admin" in request.path or "static" in request.path:
        return 
    if not session.get("admin", False):
        return render_template('coming-soon.html', session=session, animation=a(request), nofooter=True)



import app.router