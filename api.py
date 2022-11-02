from main import *
import humanize
from discord_webhook import DiscordWebhook, DiscordEmbed

def sendLog(log, uuid, ruuid, level="info"):
    wh = DiscordWebhook(url="https://discord.com/api/webhooks/1031245669958172813/3cl9VC8U5SLqrXGucL24_-uI6bTA8eLM213zcJnB0fB6s1c1kRTHj6H1rd-iiTJt4SWV")
    embed = DiscordEmbed(
        color="764af1" if level == "info" else "FF1800" if level == "error" else "00FF02" if level == "success" else "FFD800" if level == "warning" else "764af1" 
    )

    embed.set_author(
        name="Zonerender API Middleware",
        icon_url="https://media.discordapp.net/attachments/839019900978069504/1031290358124007585/Logo_700x700_-_Icon_BG.png"
    )

    embed.add_embed_field(
        name="Job UUID",
        value=uuid,
        inline=True
    )

    embed.add_embed_field(
        name="Render UUID",
        value=ruuid,
        inline=True
    )

    embed.add_embed_field(
        name="Log",
        value=log,
        inline=False
    )

    wh.add_embed(embed)
    wh.execute()

"""
|--------------------------------------------------------------------------
| Get statistics
|--------------------------------------------------------------------------
|
| Endpoint: /api/v1/stats
| Required accesses: read
|
"""

@app.route('/api/v1/stats', methods=['GET'])
def stats():
    dbc = read()
    if "Authorization" not in request.headers:
        return "Unauthorized", 401
    apikey = request.headers.get('Authorization').split(" ")[1]
    if apikey not in dbc['apikeys']:
        return jsonify({"error": "Invalid API key."}), 401
    if "read" not in dbc['apikeys'][apikey]['access']:
        return jsonify({"error": "Access denied."}), 403
    
    total = len(dbc['analytics']['renders'])
    # turn total into a string (like 1000 -> 1k) using the library "humanize"
    total = humanize.intword(total)
    words = total.split(" ")
    if len(words) == 1:
        total = words[0]
    else:
        word = words[1]
        shorts = {
            "thousand": "k",
            "million": "m",
            "billion": "b",
            "trillion": "t",
            "quadrillion": "q",
        }
        total = total.replace(" "+word, shorts[word])



    stats = {
        "renders": {
            "total": {
                "exact": len(dbc['analytics']['renders']),
                "humanized": total
            }
        }
    }

    return jsonify(stats)

"""
|--------------------------------------------------------------------------
| PayPal | Create payment
|--------------------------------------------------------------------------
|
| Endpoint: /api/v1/paypal/payment
| No apikkey required
|
"""

@app.route('/api/v1/paypal/payment/<jobuuid>', methods=['POST'])
def paypal_payment(jobuuid):
    # For demo purposes, we have a demo payment
    job = jobs[jobuuid]
    dbc = read()
    template = dbc['products'][job['templateid']]
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:5001/api/v1/paypal/payment/execute/"+jobuuid,
            "cancel_url": "http://127.0.0.1:5001/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": template['name'],
                    "sku": jobuuid,
                    "price": job["payment"]["price"],
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "currency": "USD",
                "total": job["payment"]["price"]
            },
            "description": "Payment for render job "+jobuuid
        }]
    })

    if payment.create():
        print("Payment created successfully")
        jobs[jobuuid]['paypal'] = {
            "paid": False,
            "payment_id": payment.id
        }
        return jsonify({'paymentID' : payment.id})
    else:
        print(payment.error)
        return jsonify({"error": payment.error})

"""
|--------------------------------------------------------------------------
| PayPal | Execute payment
|--------------------------------------------------------------------------
|
| Endpoint: /api/v1/paypal/payment/execute
| No apikkey required
|
"""

@app.route('/api/v1/paypal/payment/execute/<jobuuid>', methods=['POST'])
def paypal_payment_execute(jobuuid):
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')

        """
        Stuff we now have access to:
        payment.id
        payment.transactions[0].item_list.items[0].sku
        payment.transactions[0].item_list.items[0].name
        payment.transactions[0].item_list.items[0].price
        payment.transactions[0].item_list.items[0].currency
        payment.transactions[0].item_list.items[0].quantity
        payment.transactions[0].amount.total
        payment.transactions[0].amount.currency
        payment.transactions[0].description
        """

        # Let's verify that the jobuuid is the same as the one in the payment
        if payment.transactions[0].item_list.items[0].sku == jobuuid:
            if jobs[jobuuid]['paypal']['payment_id'] == payment.id:
                jobs[jobuuid]['paypal']['paid'] = True
                success = True
            else:
                print("Payment ID mismatch")
        else:
            print("Job UUID mismatch")

    else:
        print(payment.error)

    return jsonify({'success' : success})

"""
|--------------------------------------------------------------------------
| Checkout | Form
|--------------------------------------------------------------------------
|
| Endpoint: /api/v1/checkout/<jobuuid>/form
| No apikkey required
|
"""

@app.route('/api/v1/checkout/<jobuuid>/form', methods=['POST'])
def checkout_form(jobuuid):
    fields = {
        "first_name": request.json['firstName'],
        "last_name": request.json['lastName'],
        "email": request.json['emailAddress'],
        "discord": request.json['discordHandle']
    }

    jobs[jobuuid]['details'] = fields

    sendLog("""
Checkout form filled out
```
%s
```
""" % j.dumps(fields, indent=4), jobuuid, "N/A")
    return True







