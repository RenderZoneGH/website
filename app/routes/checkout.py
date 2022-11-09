from app import flask, request, render_template, redirect, url_for, flash, session, jobs
from app.util.animation import a
from app.util.db import read
import uuid as u

def init(route):
    @flask.route(route, methods=['GET', 'POST'])
    def checkout(uuid):
        if request.method == "GET":
            dbc = read()
            products = dbc['products']
            if uuid in jobs:
                job = jobs[uuid]
                if job['templateid'] not in products:
                    flash("Unknown product!", "error")
                    return redirect(url_for('index'))
                product = products[job['templateid']]
                return render_template("checkout.html", session=session, db=dbc, animation=a(), product=product, uuid=uuid, job=job)
            else:
                flash("Unknown product!", "error")
                return redirect(url_for('index'))
        # Post (ignore for now)
        return redirect(url_for('index'))