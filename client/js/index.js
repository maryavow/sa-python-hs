document.addEventListener('DOMContentLoaded', async() => {
  
  decodeURIComponent

  

  document.getElementById('checkout').addEventListener('click', function() {
    //see which book was selected and do a server call for title and price
    const urlParams = new URLSearchParams(window.location.search);
    const item = urlParams.get('item');

    const checkout =  fetch("/checkout?param=${item}", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
       
    }).then(res => res.json())
   
    document.getElementById('item').innerText = checkout.item;
    document.getElementById('title').innerText = checkout.title;
    document.getElementById('amount').innerText = checkout.amount;
    

    //now redirect
    window.location.href = `view/checkout.html?item=${item}`;
  });


  
});

