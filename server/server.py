#! /usr/bin/env python3.6
import stripe
import json
import os

from flask import Flask, g, render_template, jsonify, request , session #, send_from_directory
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

# For sample support and debugging, not required for production:
stripe.set_app_info(
    'stripe-samples/your-sample-name',
    version='0.0.1',
    url='https://github.com/stripe-samples')

stripe.api_version = os.getenv("STRIPE_API_VERSION")  #'2020-08-27'
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

static_dir = str(os.path.abspath(os.path.join(__file__ , "..", os.getenv("STATIC_DIR"))))
app = Flask(__name__, static_folder=static_dir, static_url_path="", template_folder=static_dir)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

#---------------------------------------------------------------------------
#the base page for the app
@app.route('/', methods=['GET'])
def get_root():
    return render_template('index.html')

#---------------------------------------------------------------------------
#route to get the publishable key from the environment variable
#this is used in the frontend to create the stripe instance
#and to create the payment intent
@app.route('/config', methods=['GET'])
def get_config():
    return jsonify({'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY')})


#---------------------------------------------------------------------------
#route for dummy database to get the item selected
@app.route('/checkout', methods=['GET'])
def checkout():
    # Just hardcoding amounts here to avoid using a database
    item = request.args.get('item')
    title = None
    amount = None
    error = None
    #session.pop('sess_amount', None)
    #session.pop('sess_item', None)

    if item == '1':
        title = 'The Art of Doing Science and Engineering'
        amount = 2300
    elif item == '2':
        title = 'The Making of Prince of Persia: Journals 1985-1993'
        amount = 2500
    elif item == '3':
        title = 'Working in Public: The Making and Maintenance of Open Source'
        amount = 2800
    else:
        # Included in layout view, feel free to assign error
        error = 'No item selected'

    #set g data
    g.title = title
    g.amount = amount
    
    # set the session variable to the amount and item selected
    session['sess_amount'] = amount
    session['sess_item'] = item
    return jsonify({"title": title, "amount": amount, "item": item, "error": error} )
    

#---------------------------------------------------------------------------
#set the g.amount from the session - dont want the client to manipulate it
@app.before_request
def set_g_amount():
    # Set g.amount from the session if it exists
    if 'sess_amount' in session:
        g.amount = session['sess_amount']

#---------------------------------------------------------------------------
#route to create the payment intent in stripe
@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    # Ensure g.amount is set
    if not hasattr(g, 'amount') or g.amount is None:
        return jsonify({"error": "Amount not set. Please start from the checkout page."}), 400

    payment_intent = stripe.PaymentIntent.create(
        #lookup the price in the hardcoded file that was presented in frontend
        amount=g.amount,
        currency="aud",
        automatic_payment_methods={
            'enabled': True,
        },
      #payment_method_types=["card"],
    )
    #as the return for POST, we provide clientsecret back to the client as part of teh oayment intent creation
    return jsonify(clientSecret=payment_intent.client_secret)


#---------------------------------------------------------------------------
#if you want to use webhooks, you can set up a webhook endpoint to receive events from Stripe
@app.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            #data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
       # data = request_data['data']
        event_type = request_data['type']
    #data_object = data['object']

    if event_type == 'payment_intent.succeeded':
        print('💰 Payment received!')


    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app
    app.run(port=4242, debug=True)
