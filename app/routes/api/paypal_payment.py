from app import flask, request, render_template, redirect, url_for, flash, session, jobs, paypalrestsdk
from app.util.animation import a
from app.util.db import read
from app.util.env import env
import uuid as u
import json as j
import os


def init(route):
    @flask.route("/api/v1/"+route, methods=['POST'])
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
            return j.dumps({'paymentID' : payment.id})
        else:
            print(payment.error)
            return j.dumps({"error": payment.error})