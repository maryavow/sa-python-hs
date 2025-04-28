# Harish Srivastava 28-Apr-2025
# Steps of how I built it, resources used and specific changes I did to the sample python program provided as part of the process.

------------------------------------------------------------------------------------------------------
# A. How to build, configure and run your application

Please refer to /server/README.md for instructions

## Application Overview
This is a 3-page application that demonstrates a simple e-commerce flow using Stripe APIs for payment processing.

### Pages:
1. **Page 1: `index.html` / `index.js`**
   - Base navigation page where customers can select one of three books to purchase.
   - Redirects the customer to the checkout page.

2. **Page 2: `checkout.html` / `checkout.js`**
   - Checkout functionality where Stripe APIs are called:
     - Fetches the publishable key.
     - Creates a payment intent using the client secret.
     - Renders the Stripe Payment Element for secure payment.

3. **Page 3: `complete.html` / `complete.js`**
   - Confirmation page that displays the `payment_intent_id` and the transaction status.

## Prerequisites:
1. Install Python 3.6+ and Flask.
2. Install dependencies listed in `requirements.txt`.
3. Set up a `.env` file with the following keys:
   - `STRIPE_SECRET_KEY`
   - `STRIPE_PUBLISHABLE_KEY`
   - `FLASK_SECRET_KEY`
   - `STRIPE_API_VERSION`
   - `STATIC_DIR`
   
## Testing the application
1. Follow the instructions in `/server/README.md` to set up the environment.
2. Start the Flask server:
   ```bash
   python server.py
3. Open your browser and navigate to http://localhost:4242
4. Test the checkout flow using Stripe's test card data:
    - Card Number: 4242 4242 4242 4242
    - Expiration Date: Any future date
    - CVC: Any 3-digit number 
    - [See https://stripe.com/docs/testing]


------------------------------------------------------------------------------------------------------
# B. How does the solution work? Which Stripe APIs does it use? How is my application architected?

## Architecture of application
1. Client side: 
    - HTML, JavaScript, CSS, and static assets are located under /client.
    - Handles user interactions and renders the Stripe Payment Element.

2. Server-Side:
    - Python Flask application located in /server/server.py.
    - Handles API routes for:
        /config: Fetches the publishable key.
        /checkout: Provides item details (stubbed database).
        /create-payment-intent: Creates a payment intent using Stripe APIs.
        
3. Database Stub:
    - The /checkout endpoint acts as a stub for a database, providing hardcoded item details.

4. Folder Structure 
    /client
        /css
        /images
        /js
        /view
    /server
        server.py
        .env

## Stripe APIs and Concepts used

1. Payment Intent API:
        Creates a payment intent with the specified amount and currency.
2. Payment Element:
        Renders a secure payment form on the client side.
3.  Stripe Dashboard:
        Used to configure payment methods (e.g., Card, Afterpay, Klarna).

------------------------------------------------------------------------------------------------------
# C. * How did I approach this problem? Which docs did I use to complete the project? What challenges did I encounter?

## Framework : 
1. FLASK

## IDE : 
1. VSCode on Mac
2. Extensions used 
    1. Python
    2. Pthon debugger
    3. Pylance
    4. Ruff
    5. Stripe
    6. Github Copilot
    7. Github Copilot chat

## Stripe Dashboard Configuration
1. Activated the payment methods CARD, AFTERPAY, KLARNA
2. Copied the API keys from the Stripe developer dashbiard https://dashboard.stripe.com/test/apikeys to the .env file

## Stripe documentations and other resources used
1. Sample code as provided in email : https://github.com/marko-stripe/sa-takehome-project-python/tree/master
2. Payment Element Docs: https://docs.stripe.com/payments/payment-element?locale=en-GB
3. Stripe Quickstart Guide  https://docs.stripe.com/payments/quickstart
4. Youtube video : Video Payment Element using python https://www.youtube.com/watch?v=tCSbCk5j3Tk
5. Payment Intent Docs: https://docs.stripe.com/payments/payment-intents

## Challenges encountered on Server side:  server.py, and .env
1. used  g, session from flask to ensure sensitive information (e.g., amount) is not exposed or be alteed by client
2. created a secret flask key in .env
3. Defined the /config and /create-payment-intent routes
4. Made adjustements to /checkout route to use g and store the anount so that it can't be altered on client side
5. added STRIPE_API_VERSION and FLASK_SECRET_KEY to .env


------------------------------------------------------------------------------------------------------
# D. How I might extend this if I was building a more robust instance of the same application.

## User Experience
1. Authenticated experience
2. Ensure responsiveness in the app across device form factors
3. Use locale to pull language/currency. At the moment its kinda hardocded to EN/AUD on server side
4. Better error handling, and confirmation messages before url redirects for better UX

## Application non-functional
 
1. Using database tier and a cart framework
2. Havent done any server-side scaling or other non-functional like accessibility
3. Look at reusability
4. Have very lightly used session vars
5. Possibly explore Websockets which I haven't in this submission
6. Better logging on server side
7. have ROUTE to get the CLIENT_SECRET rather than reliance on URL parameters


## Get support

If you found a bug or want to suggest a new [feature/use case/sample], please [file an issue](../../issues).

If you have questions, comments, or need help with code, we're here to help:

- on [Discord](https://stripe.com/go/developer-chat)
- on Twitter at [@StripeDev](https://twitter.com/StripeDev)
- on Stack Overflow at the [stripe-payments](https://stackoverflow.com/tags/stripe-payments/info) tag

Sign up to [stay updated with developer news](https://go.stripe.global/dev-digest).

## Author(s)

[@adreyfus-stripe](https://twitter.com/adrind)

## Contributing

If you'd like to contribute to this sample, please check out the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md)

## Code of conduct

This repository has a [code of conduct](CODE_OF_CONDUCT.md), please read it before opening an issue or a PR.
# sa-python-hs
