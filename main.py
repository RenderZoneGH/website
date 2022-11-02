import datetime
from itertools import product
import os
import sys
from api import *
import time
import socketio as s
import uuid as u
from flask import *
import json as j
import random
import jinja2
import requests
from functools import wraps
import paypalrestsdk
import bcrypt
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET")


jobs = {}


def read():
    with open(os.getenv("DB_FILE"), 'r') as f:
        return j.load(f)


def write(data):
    with open(os.getenv("DB_FILE"), 'w') as f:
        j.dump(data, f)

class colours:
    SUCCESS = '\033[92m'
    INFO = '\033[94m'
    FAIL = '\033[91m'
    DEFAULT = '\033[0m'

def requires_template(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If the user doesn't have buildRepo in their session
        if not "buildRepo" in session:
            session['buildRepo'] = "base/production"
        # make sure the buildRepo is valid
        builds = read()["builds"]
        if not session['buildRepo'] in builds.keys():
            session['buildRepo'] = "base/production"
        return f(*args, **kwargs)
    return decorated_function

def getTemplate(buildRepo, templateid):
    builds = read()["builds"]
    build = builds[buildRepo]
    templates = build["templates"]
    template = templates[templateid]
    return template

def onlyBuild(buildRepo):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session['buildRepo'] != buildRepo:
                return fallback('Invalid route.', 404)
        return decorated_function
    return decorator

sio = s.Client()

paypalrestsdk.configure({
    "mode": "sandbox" if os.getenv("ENVIROMENT") == "dev" else "live",
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")})
    

@app.route('/')
@requires_template
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

    ani = True if "ani" in request.args else False
    return render_template(getTemplate(session["buildRepo"], "index"), products=dpr, session=session, db=dbc, animation=ani)


@app.route('/browse')
@requires_template
def browse():
    dbc = read()

    products = list(dbc['products'].values())

    # Pagination
    page = 1
    if "page" in request.args:
        page = int(request.args.get("page"))
    if page < 1:
        page = 1
    
    inpage = 12
    pages = len(products) / inpage
    if pages % 1 != 0:
        pages = int(pages) + 1
    else:
        pages = int(pages)
    if page > pages:
        page = pages
    
    start = (page - 1) * inpage
    end = start + inpage
    products = products[start:end]

    pages = list(range(1, pages+1))
    current = page


    ani = True if "ani" in request.args else False
    return render_template(getTemplate(session["buildRepo"], "browse"), products=products, session=session, db=dbc, animation=ani, pages=pages, current=current)


@app.route('/generate/<uuid>', methods=['GET', 'POST'])
@requires_template
def generate(uuid):
    if request.method == 'GET':
        dbc = read()
        products = dbc['products']
        if uuid in products:
            ani = True if "ani" in request.args else False
            return render_template(getTemplate(session["buildRepo"], "generate"), product=products[uuid], session=session, db=dbc, animation=ani)
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
        ret = make_response(redirect("/checkout/"+order_uuid+f"?ani=true&cX={request.args.get('cX')}&cY={request.args.get('cY')}"))
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

        return ret

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


@app.route('/generating/<uuid>')
@requires_template
def generating(uuid):
    ani = True if "ani" in request.args else False
    return render_template(getTemplate(session["buildRepo"], "generating"), session=session, db=read(), animation=ani, uuid=uuid)


@app.route("/job/<uuid>/fetch")
def job_fetch(uuid):
    if uuid in jobs:
        return jsonify(jobs[uuid])
    else:
        return jsonify({
            "status": "error",
            "error": "Unknown job!"
        })

@app.route("/checkout/<uuid>", methods=['GET', 'POST'])
@requires_template
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
            ani = True if "ani" in request.args else False
            return render_template(getTemplate(session["buildRepo"], "checkout"), session=session, db=dbc, animation=ani, product=product, uuid=uuid, job=job)
        else:
            flash("Unknown product!", "error")
            return redirect(url_for('index'))
    # Post (ignore for now)
    return redirect(url_for('index'))

@app.route("/checkout/<uuid>/render")
@requires_template
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

            
        sio.emit("job", {
            "uuid": uuid,
            "product": product
        })
        cY = request.args.get("cY")
        cX = request.args.get("cX")
        return redirect("/generating/"+uuid+f"?cX={cX}&cY={cY}&ani=true")

    else:
        flash("Unknown product!", "error")
        return redirect(url_for('index'))

def requiresAdmin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin"):
            return redirect("/admin/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin")
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

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    # the string is a float, and we need to convert the float timestamp to a datetime object
    date = datetime.datetime.fromtimestamp(date)
    native = date.replace(tzinfo=None)
    format='%Y-%m-%d %H:%M:%S'
    return native.strftime(format)


@app.route("/admin/analytics")
@requiresAdmin
def admin_analytics():
    """
    Analytics shown:
    - Amount of renders (daily)
    - Amount of money made (daily)
    - Amount of premium renders (daily)
    - Pie chart of templates used
    """
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

@app.route("/admin/jobs")
@requiresAdmin
def admin_jobs():
    dbc = read()
    recentjobs = jobs

    return render_template("admin/jobs.html.j2", session=session, db=dbc, jobs=recentjobs)

@app.route("/admin/jobs/all")
@requiresAdmin
def admin_jobs_all():
    dbc = read()

    alljobs = dbc["analytics"]["renders"]
    alljobs.reverse()

    return render_template("admin/jobs_all.html.j2", session=session, db=dbc, jobs=alljobs)

@app.route("/admin/products")
@requiresAdmin
def admin_products():
    dbc = read()
    return render_template("admin/products.html.j2", session=session, db=dbc)

@app.route("/admin/products/edit/<templateid>", methods=["GET", "POST"])
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


@app.route("/admin/products/coupons")
@requiresAdmin
def admin_products_coupons():
    dbc = read()
    return render_template("admin/coupons.html.j2", session=session, db=dbc)


@app.route("/admin/products/coupons/new", methods=["GET", "POST"])
@requiresAdmin
def admin_products_coupons_new():
    dbc = read()
    if request.method == "GET":
        return render_template("admin/edit_coupon.html.j2", session=session, db=dbc, coupon=None)

    # POST
    code = request.form.get("code")
    if code in dbc["coupons"]:
        flash("Coupon already exists!", "error")
        return redirect("/admin/products/coupons/new")

    dbc["coupons"][code] = {
        "discount": int(request.form.get("discount")),
        "used": 0
    }
    write(dbc)
    flash("Coupon created!", "success")
    return redirect("/admin/products/coupons")

@app.route("/admin/products/coupons/edit/<code>", methods=["GET", "POST"])
@requiresAdmin
def admin_products_coupons_edit(code):
    dbc = read()
    if code not in dbc["coupons"]:
        flash("Unknown coupon!", "error")
        return redirect("/admin/products/coupons")

    coupon = dbc["coupons"][code]
    if request.method == "GET":
        return render_template("admin/edit_coupon.html.j2", session=session, db=dbc, coupon=coupon, code=code)

    used = request.form.get("used")
    print(used)
    used = True if used == "on" else False

    # POST
    dbc["coupons"][code] = {
        "discount": int(request.form.get("discount")),
        "used": used
    }
    write(dbc)
    flash("Coupon updated!", "success")
    return redirect("/admin/products/coupons/edit/"+code)

@app.route("/admin/products/coupons/delete/<code>")
@requiresAdmin
def admin_products_coupons_delete(code):
    dbc = read()
    if code not in dbc["coupons"]:
        flash("Unknown coupon!", "error")
        return redirect("/admin/products/coupons")

    del dbc["coupons"][code]
    write(dbc)
    flash("Coupon deleted!", "success")
    return redirect("/admin/products/coupons")


@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == "GET":
        return render_template("admin/login.html.j2", session=session)
    else:
        password = request.form.get("password")
        username = request.form.get("username")

        dbc = read()
        if username in dbc['admins']:
            # Check password using bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), dbc['admins'][username]['password'].encode('utf-8')):
                session["admin"] = True
                session["username"] = username
                flash("Logged in!", "success")
                return redirect("/admin")
            else:
                flash("Invalid password!", "error")
                return redirect("/admin/login")
        else:
            flash("Invalid username!", "error")
            return redirect("/admin/login")

@app.route("/admin/logout")
@requiresAdmin
def admin_logout():
    session["admin"] = False
    session["username"] = None
    return redirect("/admin/login")

@app.route("/coupon/checkout/<jobid>", methods=["POST"])
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

@sio.event
def json(data):
    print(colours.INFO, 'Render API sent JSON: '+str(data), colours.DEFAULT)
    # if data contains "done" or "error" then send it to the client
    if "done" in data:
        r = requests.get(data['url'], allow_redirects=True)
        open('static/img/exported/'+data['uuid']+'.gif', 'wb').write(r.content)

        jobs[data['uuid']]['done'] = True
        jobs[data['uuid']]['url'] = data['url']
        jobs[data['uuid']]['display'] = data['display']
        print(colours.SUCCESS, 'Job ' +
              data['uuid']+' is done!', colours.DEFAULT)

        dbc = read()
        dbc['analytics']['renders'].append({
            "uuid": data['uuid'],
            "templateid": jobs[data['uuid']]['templateid'],
            "time": time.time()
        })

        if "payment" in jobs[data['uuid']]:
            dbc['analytics']['renders'][-1]["payment"] = jobs[data['uuid']]['payment']
            dbc['analytics']['renders'][-1]["payment"]["paypal"] = jobs[data['uuid']]['paypal']
        
        write(dbc)

    elif "error" in data:
        jobs[data['uuid']]['done'] = True
        jobs[data['uuid']]['error'] = data['error']
        jobs[data['uuid']]['display'] = data['display']
        print(colours.FAIL, 'Job '+data['uuid']+' failed!', colours.DEFAULT)
    elif "update" in data:
        jobs[data['uuid']]['display'] = data['display']
        print(colours.INFO, 'Job '+data['uuid']+' updated!', colours.DEFAULT)
 

@sio.event
def rnode(data):
    print(colours.INFO, 'Render Node update: '+str(data), colours.DEFAULT)
    if "uuid" in data:
        uuid = data['uuid']
        jobs[uuid]["display"] = "In queue" if data["details"]["state"] == "queued" else "Getting started..." if data["details"]["state"] == "started" else "Rendering..."
        jobs[uuid]["render"]["progress"] = data["details"]['renderProgress']


@sio.event
def disconnect():
    print(colours.FAIL, 'Disconnected from Render API', colours.DEFAULT)
    # try to reconnect every 5 seconds
    rfail = True
    while True:
        try:
            sio.connect(os.getenv("API_CLIENT_URL"))
            rfail = False
            break
        except:
            time.sleep(5)

@app.route('/build/set/<key>')
def build_set(key):
    builds = read()['builds']
    buildRepo = request.args.get("repo")
    if buildRepo in builds:
        if builds[buildRepo]["key"] == key:
            session["buildRepo"] = buildRepo
            return redirect("/")
    alert = """
    <script>
        alert("Invalid key!");
        window.location.href = "/";
    </script>
    """
    return alert
    
from api import *

if __name__ == '__main__':
    if os.getenv("API_CLIENT_ENABLED") == "true":
        try:
            sio.connect(os.getenv("API_CLIENT_URL"))
        except:
            print(colours.FAIL, "Failed to connect to the render node!", colours.DEFAULT)
            rfail = True

    app.run(debug=True if os.getenv("ENVIORMENT") == "dev" else False, port=os.getenv("PORT"))

