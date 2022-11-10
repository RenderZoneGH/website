from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read, write
from app.util.decorators.admin import requiresAdmin

def init(route):
    @flask.route("/admin/products/coupons/new", methods=["GET", "POST"])
    @requiresAdmin
    def admin_products_coupons_new():
        dbc = read()
        if request.method == "GET":
            return render_template("admin/edit_coupon.html.j2", session=session, db=dbc, coupon=None)

        # POST
        code = request.form.get("code")
        if code in dbc["coupons"]:
            flash("Coupon already exists!", "error")
            return redirect("/admin/products/coupons/new")

        dbc["coupons"][code] = {
            "discount": int(request.form.get("discount")),
            "used": 0
        }
        write(dbc)
        flash("Coupon created!", "success")
        return redirect("/admin/products/coupons")