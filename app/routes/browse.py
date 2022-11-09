from app import flask, request, render_template, redirect, url_for, flash, session
from app.util.animation import a
from app.util.db import read

def init(route):
    @flask.route(route)
    def browse():
        dbc = read()
        products = list(dbc['products'].values())
        return render_template("browse.html", products=products, session=session, db=dbc, animation=a(request))
