from flask import Flask, render_template, request, redirect, url_for, flash, session
import socketio
import dotenv
from app.util.env import env
import paypalrestsdk

flask = Flask(__name__)
flask.config['SECRET_KEY']  = env("SECRET_KEY", "secret")
sio = socketio.Client()

jobs = {}

paypalrestsdk.configure({
    "mode": "sandbox" if env("ENVIRONMENT", "prod") == "dev" else "live",
    "client_id": env("PAYPAL_CLIENT_ID", "cid"),
    "client_secret": env("PAYPAL_CLIENT_SECRET", "pcs")
})


import app.router