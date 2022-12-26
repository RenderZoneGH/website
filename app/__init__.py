import datetime
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
    if "admin" in request.path or "static" in request.path or "api" in request.path or "robots.txt" in request.path or "join" in request.path:
        return 
    if not session.get("admin", False) or not (session.get("accesskey", "key") == env("cskey", "PJNijeoksnosjnwojn28ienojsniehj3nskns8n3u3nojwnj3n4ij3ijsiwpkwmpwm92kkmqpkw0ke9j3ij3ksns9enk2o")):
        return render_template('coming-soon.html', session=session, animation=a(request), nofooter=True)

@flask.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    # the string is a float, and we need to convert the float timestamp to a datetime object
    date = datetime.datetime.fromtimestamp(date)
    native = date.replace(tzinfo=None)
    format='%Y-%m-%d %H:%M:%S'
    return native.strftime(format)

import app.router
import app.connection

if not env("RENDER_API_DISABLED", False):
    sio.connect(env("RENDER_API_URL", "http://localhost:3000"))

