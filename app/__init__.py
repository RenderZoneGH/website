from flask import Flask, render_template, request, redirect, url_for, flash, session
import socketio
import dotenv
from app.util.env import env

flask = Flask(__name__)

sio = socketio.Client()

import app.router