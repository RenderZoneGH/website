from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read
from app.util.decorators.admin import requiresAdmin


def init(route):
    @flask.route("/admin/products/coupons")
    @requiresAdmin
    def admin_products_coupons():
        dbc = read()
        return render_template("admin/coupons.html.j2", session=session, db=dbc)