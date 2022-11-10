from app import flask, request, render_template, redirect, flash, session, jobs
from app.util.animation import a
from app.util.db import read, write
 
def init(route):
    @flask.route(route, methods=["POST"])
    def coupon_checkout(uuid):
        coupon = request.form["coupon"]
        if uuid not in jobs:
            flash("Unknown product!", "error")
            return redirect("/")
        dbc = read()
        print(coupon)
        if coupon in list(dbc["coupons"].keys()):
            if dbc["coupons"][coupon]["used"] == False:
                dbc["coupons"][coupon]["used"] = True
                write(dbc)

                jobs[uuid]["payment"]["discount"] = dbc["coupons"][coupon]["discount"]
                jobs[uuid]["payment"]["price"] = jobs[uuid]["payment"]["price"] - (jobs[uuid]["payment"]["price"] * (dbc["coupons"][coupon]["discount"] / 100))
                jobs[uuid]["payment"]["price"] = round(jobs[uuid]["payment"]["price"], 2)
                jobs[uuid]["payment"]["coupon"] = coupon
                return redirect("/checkout/"+uuid+f"?ani=true&cX={request.args.get('cX')}&cY={request.args.get('cY')}")
            else:
                flash("Coupon already used!", "error")
                return redirect("/checkout/"+uuid+f"?ani=true&cX={request.args.get('cX')}&cY={request.args.get('cY')}")
        else:
            flash("Invalid coupon!", "error")
            return redirect("/checkout/"+uuid+f"?ani=true&cX={request.args.get('cX')}&cY={request.args.get('cY')}")
