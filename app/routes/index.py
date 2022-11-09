from app import flask, request, render_template, redirect, url_for, flash, session
from app.util.animation import a
from app.util.db import read
import random

def init(route):
    @flask.route(route)
    def index():
        dbc = read()
        # get 4 random products to show on the home page
        products = dbc['products']
        
        p = {
            "paid": [],
            "free": []
        }

        for pv in products.values():
            if pv["price"] == 0:
                p["free"].append(pv)
            else:
                p["paid"].append(pv)

        
        # dbc['products'] is a dict "uuid": {product data}
        # so we need to pick 5 random keys from the dict
        # and then get the values of those keys
        # if there are less than 5 products, use the same system but make it resistent to errors
        # we need to get 5 random free products and 5 random paid products

        # get 5 random free products
        free = []
        if len(p["free"]) < 5:
            free = p["free"]
        else:
            free = random.sample(p["free"], 5)

        # get 5 random paid products
        paid = []
        if len(p["paid"]) < 5:
            paid = p["paid"]
        else:
            paid = random.sample(p["paid"], 5)

        dpr = {
            "free": free,
            "paid": paid
        }

        print(dpr)

        return render_template("index.html", products=dpr, session=session, db=dbc, animation=a(request))


