from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read
from app.util.decorators.admin import requiresAdmin
import datetime
from app.util.db import read, write

def init(route):
    @flask.route("/admin/products/edit/<templateid>", methods=["GET", "POST"])
    @requiresAdmin
    def admin_products_edit(templateid):
        dbc = read()
        if templateid not in dbc["products"]:
            flash("Unknown product!", "error")
            return redirect("/admin/products")

        product = dbc["products"][templateid]
        if request.method == "GET":
            dailyrenders = {}

            for p in dbc["analytics"]["renders"]:   
                if p["templateid"] == templateid:
                    date = datetime.datetime.fromtimestamp(p["time"]).strftime('%Y-%m-%d')
                    if date not in dailyrenders:
                        dailyrenders[date] = 0
                    dailyrenders[date] += 1

                    
            return render_template("admin/products_edit.html.j2", session=session, db=dbc, product=product, dailyrenders=dailyrenders)

        # POST
        prod = {
            "name": request.form.get("name"),
            "price": int(request.form.get("price")),
            "category": request.form.get("category"),
            "tags": request.form.get("tags").split(","),
            "uuid": templateid,
            # retriving the origianl values becouse not all values are in the form
            "preview": product["preview"],
            "preview-mockup": product["preview-mockup"],
            "attr": product["attr"],
            "ae": product["ae"],
        }

        for t in prod["tags"]:
            t.strip()
            if t == "":
                prod["tags"].remove(t)

        dbc["products"][templateid] = prod
        write(dbc)
        flash("Product updated!", "success")
        return redirect("/admin/products/edit/"+templateid)