from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read
from app.util.decorators.admin import requiresAdmin
 
def init(route):
    @flask.route(route)
    @requiresAdmin
    def admin_logout():
        session["admin"] = False
        session["username"] = None
        return redirect("/admin/login")