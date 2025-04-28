document.addEventListener('DOMContentLoaded', async() =>{
    
    decodeURIComponent

    //see which book was selected and do a server call for title and price
    const urlParams = new URLSearchParams(window.location.search);
    const item = urlParams.get('item');
    let fetchurl = "/checkout?item=" + item;
    //console.log("fetchurl: " + fetchurl)

    //get the checkout information from the server
    const checkout =  await fetch(fetchurl, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
       
    }).then(res => res.json())
  
    //console.log("jsonCheckout.title: " + checkout.title)
    //console.log("jsonCheckout.item: " + checkout.item)
    //console.log("jsonCheckout.amount: " + checkout.amount)
  

    //set the title and amount in the html elements by parsing the json response
    document.getElementById('item').innerText = checkout.item;
    document.getElementById('title').innerText = checkout.title;
    document.getElementById('amount').innerText = checkout.amount/100; //server gives amount in cents, so divide by 100 to get dollars
    
    
    //Its a 2 step process from here.
    //Step 1: init istripe by getting publishable key from server
    const {publishableKey} = await fetch("/config").then(res => res.json())
    const stripe = Stripe(publishableKey);

    

    //Step 2: init payment intent by passing client secret to stripe
    const {clientSecret} = await fetch("/create-payment-intent", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json())
    

    const elements = stripe.elements({clientSecret})
    const paymentElement = elements.create("payment")
    paymentElement.mount("#payment-element")

    //handle form submission onClick of PAY button
    const form = document.getElementById("payment-form")
    form.addEventListener("submit", async(e) => {
        e.preventDefault();
        
        const {error}   = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: window.location.href.split("/view")[0] +"/view/complete.html"
               
            }
        })
        if(error){
            //show error message
            const messages = document.getElementById("error-messages")
            //console.log("payment error: " + error.message),
            messages.innerText = error.message;
        }
        
       
    })
})