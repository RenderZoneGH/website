from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read
 
def init(route):
    @flask.route(route)
    def join():
        session["accesskey"] = request.args.get("key", "key")
        return redirect("/")