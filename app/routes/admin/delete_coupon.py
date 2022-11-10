from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read, write
from app.util.decorators.admin import requiresAdmin

def init(route):
    @flask.route("/admin/products/coupons/delete/<code>")
    @requiresAdmin
    def admin_products_coupons_delete(code):
        dbc = read()
        if code not in dbc["coupons"]:
            flash("Unknown coupon!", "error")
            return redirect("/admin/products/coupons")

        del dbc["coupons"][code]
        write(dbc)
        flash("Coupon deleted!", "success")
        return redirect("/admin/products/coupons")