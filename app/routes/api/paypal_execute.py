from app import flask, request, render_template, redirect, flash, session, jobs, paypalrestsdk
from app.util.db import read, write
import json as j

def init(route):
    @flask.route('/api/v1/paypal/payment/execute/<jobuuid>', methods=['POST'])
    def paypal_payment_execute(jobuuid):
        success = False
    
        payment = paypalrestsdk.Payment.find(request.form['paymentID'])
    
        if payment.execute({'payer_id' : request.form['payerID']}):
            print('Execute success!')
    
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
    
        return j.dumps({'success' : success})
    