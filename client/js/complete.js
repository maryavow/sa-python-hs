document.addEventListener("DOMContentLoaded", async () => {
    
    //init istripe by getting publishable key from server
    const { publishableKey } = await fetch("/config").then((res) => res.json());
    const stripe = Stripe(publishableKey);

    //get the client secret from the url
    const urlParams = new URLSearchParams(window.location.href);
    const clientSecret = urlParams.get("payment_intent_client_secret");

    const {paymentIntent} = await stripe.retrievePaymentIntent(clientSecret);
    

    const paymentIntentPre = document.getElementById("payment-intent");
    paymentIntentPre.innerText = JSON.stringify(paymentIntent, null, 2);
    //console.log("paymentIntent: " + paymentIntentPre.innerText);

    //set the title and amount in the html elements by parsing the json response
    document.getElementById('payment_intent_id').innerText = paymentIntent.id;
    document.getElementById('transaction_status').innerText = paymentIntent.status;
    document.getElementById('amount').innerText = paymentIntent.amount/100; //server gives amount in cents, so divide by 100 to get dollars
    document.getElementById('currency').innerText = paymentIntent.currency;
  
   
})
