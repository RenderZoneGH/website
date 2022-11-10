from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read
from app.util.decorators.admin import requiresAdmin
import datetime

def init(route):
    @flask.route(route)
    @requiresAdmin
    def admin_analytics():
        dbc = read()
        ana = {
            "date_renders": {},
            "date_money": {},
            "template_renders": {}
        }

        for p in dbc["analytics"]["renders"]:
            if "payment" in p:
                if "price" in p["payment"]:
                    date = datetime.datetime.fromtimestamp(p["time"]).strftime('%Y-%m-%d')
                    if date not in ana["date_money"]:
                        ana["date_money"][date] = 0
                    ana["date_money"][date] += p["payment"]["price"]
            date = datetime.datetime.fromtimestamp(p["time"]).strftime('%Y-%m-%d')
            if date not in ana["date_money"]:
                ana["date_money"][date] = 0
            if date not in ana["date_renders"]:
                ana["date_renders"][date] = 0
            ana["date_renders"][date] += 1

            if p["templateid"] not in ana["template_renders"]:
                ana["template_renders"][p["templateid"]] = 0
            ana["template_renders"][p["templateid"]] += 1
        
        return render_template("admin/analytics.html.j2", session=session, db=dbc, ana=ana)