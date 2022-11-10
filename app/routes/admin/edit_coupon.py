from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read, write
from app.util.decorators.admin import requiresAdmin

def init(route):
    @flask.route("/admin/products/coupons/edit/<code>", methods=["GET", "POST"])
    @requiresAdmin
    def admin_products_coupons_edit(code):
        dbc = read()
        if code not in dbc["coupons"]:
            flash("Unknown coupon!", "error")
            return redirect("/admin/products/coupons")

        coupon = dbc["coupons"][code]
        if request.method == "GET":
            return render_template("admin/edit_coupon.html.j2", session=session, db=dbc, coupon=coupon, code=code)

        used = request.form.get("used")
        print(used)
        used = True if used == "on" else False

        # POST
        dbc["coupons"][code] = {
            "discount": int(request.form.get("discount")),
            "used": used
        }
        write(dbc)
        flash("Coupon updated!", "success")
        return redirect("/admin/products/coupons/edit/"+code)