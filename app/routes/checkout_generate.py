from app import flask, request, render_template, redirect, url_for, flash, session, jobs
from app.util.animation import a
from app.util.db import read
import uuid as u
import jinja2
import json as j

def init(route):
    @flask.route(route)
    def checkout_render(uuid):
        if uuid in jobs:
            job = jobs[uuid]
            if job['templateid'] not in read()['products']:
                flash("Unknown product!", "error")
                return redirect(url_for('index'))
            # Let's verify the payment
            if job.get("paypal", {"paid": False})["paid"] == False and job['payment']['price'] != 0:
                flash("Payment not paid!", "error")
                return redirect(url_for('index'))

            
            # Let's render the product
            product = read()['products'][job['templateid']]
            # product["ae"]["assets"] is a list of assets. It might contain calls for fields using Jinja2
            # so we need to replace those with the values from the form
            
            assets = j.dumps(product["ae"]["assets"])
            # run assets through jinja2
            assets = jinja2.Template(assets).render(fields=job['fields'])
            assets = j.loads(assets)

            product["ae"]["assets"] = assets

            """
            sio.emit("job", {
                "uuid": uuid,
                "product": product
            })
            """
            # This code will start working once the WebSocket server is implemented
            cY = request.args.get("cY")
            cX = request.args.get("cX")
            return redirect("/generating/"+uuid+f"?cX={cX}&cY={cY}&ani=true")

        else:
            flash("Unknown product!", "error")
            return redirect(url_for('index'))