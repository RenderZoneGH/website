from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read
from app.util.decorators.admin import requiresAdmin 

def init(route):
    @flask.route("/admin/products")
    @requiresAdmin
    def admin_products():
        dbc = read()
        return render_template("admin/products.html.j2", session=session, db=dbc)