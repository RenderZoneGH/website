from app import flask, request, render_template, redirect, flash, session, jobs
from app.util.animation import a
from app.util.db import read, write
 
def init(route):
    @flask.route(route, methods=["POST"])
    def coupon_checkout(jobid):
        coupon = request.form["coupon"]
        dbc = read()
        print(coupon)
        if coupon in list(dbc["coupons"].keys()):
            if dbc["coupons"][coupon]["used"] == False:
                dbc["coupons"][coupon]["used"] = True
                write(dbc)

                jobs[jobid]["payment"]["discount"] = dbc["coupons"][coupon]["discount"]
                jobs[jobid]["payment"]["price"] = jobs[jobid]["payment"]["price"] - (jobs[jobid]["payment"]["price"] * (dbc["coupons"][coupon]["discount"] / 100))
                jobs[jobid]["payment"]["price"] = round(jobs[jobid]["payment"]["price"], 2)
                jobs[jobid]["payment"]["coupon"] = coupon
                return redirect("/checkout/"+jobid+f"?ani=true&cX={request.args.get('cX')}&cY={request.args.get('cY')}")
            else:
                flash("Coupon already used!", "error")
                return redirect("/checkout/"+jobid+f"?ani=true&cX={request.args.get('cX')}&cY={request.args.get('cY')}")
        else:
            flash("Invalid coupon!", "error")
            return redirect("/checkout/"+jobid+f"?ani=true&cX={request.args.get('cX')}&cY={request.args.get('cY')}")
