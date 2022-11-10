from app import flask, request, render_template, redirect, url_for, flash, session, jobs
from app.util.animation import a as an
from app.util.db import read
import uuid as u
import os

def init(route):
    @flask.route(route, methods=['GET', 'POST'])
    def generate(uuid):
        if request.method == 'GET':
            dbc = read()
            products = dbc['products']
            if uuid in products:
                return render_template('generate.html', session=session, animation=an(request), product=products[uuid], db=dbc)
            else:
                flash("Unknown product!", "error")
                return redirect(url_for('index'))

        # Post
        dbc = read()
        products = dbc['products']
        if uuid not in products:
            flash("Unknown product!", "error")
            return redirect(url_for('index'))

        product = products[uuid]
        fields = {}
        try:
            for a in product['attr']:
                value = product['attr'][a]
                if not value['config']:
                    continue
                if value['type'] == 'file':
                    if not request.files[a]:
                        flash("Missing file!", "error")
                        return redirect(url_for('generate', uuid=uuid))
                    imageuuid = str(u.uuid4())
                    path = os.path.join("media/uploads", imageuuid)
                    request.files[a].save(path)
                    fields[a] = {
                        "value": imageuuid,
                        "type": "file",
                        "cost": 0 if not "cost" in value else value['cost']
                    }
                    continue
                print("Searching for "+a)
                fields[a] = {
                    "value": request.form["templ-"+a],
                    "cost": 0 if not "cost" in value else value['cost']
                }
        except KeyError:
            flash("Missing fields!", "error")
            print("Missing fields!")
            return redirect(url_for('generate', uuid=uuid))

        cost = 0
        for f in fields:
            cost += fields[f].get("cost", 0) if fields[f]["value"] != "" else 0

        cost += product['price']

        # Generate a new uuid for the order
        order_uuid = str(u.uuid4())

        if cost != 0:
            jobs[order_uuid] = {
                "done": False,
                "render": {
                    "progress": 0
                },
                "display": "Waiting for payment verification...",
                "templateid": uuid,
                "fields": fields,
                "uuid": order_uuid,
                "payment": {
                    "discount": 0,
                    "price": cost,
                    "coupon": None,
                    "costs": [
                    ]
                },
                "paypal": {
                    "paid": False,
                }
            }

            if product['price'] != 0:
                jobs[order_uuid]['payment']['costs'].append({
                    "name": product['name'],
                    "cost": product['price'],
                    "type": "template"
                })
            
            for f in fields:
                if fields[f].get("cost", 0) != 0:
                    jobs[order_uuid]['payment']['costs'].append({
                        "name": f,
                        "cost": fields[f].get("cost", 0),
                        "type": "field"
                    })

            return redirect("/checkout/"+order_uuid+f"?ani=true&cX={request.args.get('cX')}&cY={request.args.get('cY')}")

        jobs[order_uuid] = {
            "done": False,
            "render": {
                "progress": 0
            },
            "display": "Preparing...",
            "templateid": uuid,
            "uuid": order_uuid,
            "fields": fields,
            "payment": {
                "discount": 0,
                "price": 0,
                "coupon": None,
                "costs": []
            }
        }
        
        cX = request.args.get("cX")
        cY = request.args.get("cY")

        return redirect("/checkout/"+order_uuid+"/render?ani=true"+f"&cX={cX}&cY={cY}")
