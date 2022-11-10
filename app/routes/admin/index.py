from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read
from app.util.decorators.admin import requiresAdmin
import datetime

def init(route):
    @flask.route(route)
    @requiresAdmin
    def admin():
        # get the amount of money we have made (using paypal)
        dbc = read()
        money = 0
        premiums = 0

        # Daily renders
        renders = {}
        count = 0

        for p in dbc["analytics"]["renders"]:
            if "payment" in p:
                if "price" in p["payment"]:
                    money += p["payment"]["price"]
                    premiums += 1
            
            # there is a timestamp in the render 
            # we can use that to get the date
            # and then we can use that to get the amount of renders per day
            date = datetime.datetime.fromtimestamp(p["time"]).strftime('%Y-%m-%d')
            
            if date not in renders:
                renders[date] = count
            renders[date] += 1
            count += 1
            print(count)

            
        extra = {
            "money": money,
            "premiums": premiums,
            "date_renders": renders
        }

        return render_template("admin/index.html.j2", session=session, db=dbc, extra=extra)