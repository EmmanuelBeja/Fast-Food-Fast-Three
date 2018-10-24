is_logged_in = () => {
 //check if token was created/ user is logged in
 if(!window.sessionStorage.getItem('token')){
   return "not logged in";
   location.replace("/");
 }else {
   token = window.sessionStorage.getItem('token');
   return "logged in";
 }
}


cart = () => {
  //fetch cart quantity and totalprice
  return fetch('/v2/users/cart_quantity', {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
    const cart_quantity = document.getElementById('cart');
    if (cart_quantity != null) {
      cart_quantity.innerHTML = data.Cart
      const cart_total_price = document.getElementById('cart_total_price');
      cart_total_price.innerHTML = data.totalprice
    }
    res = data.message;
  }).then(message => res)
}


cart_details = () => {
  //fetch cart details
  return fetch('/v2/users/cart', {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
    if(data.message=='Logged out. Please login and update token') {
      location.replace("/login");
    }

    cart = data.Cart
    cartdata = document.getElementById('cartdata');
    if (cartdata != null) {
      cart.forEach(function(cartitem){
        cartdata.innerHTML += '<div class="list-item"><div class="box-col-8">'+cartitem.food_name+' | Price: Ksh.'+cartitem.price+' | Qty: '+cartitem.quantity+'</div></div>';
      });
      cartdata.innerHTML +='<div class="list-item"><div class="box-col-8">Total: Ksh. '+data.totalprice+'</div></div>'
    }
    res = data.message;
  }).then(message => res)
}


//place order function
order = (adress) => {
  if (adress == undefined) {
    adress = document.getElementById('adress').value;
  }
  return fetch('/v2/users/orders', {
    method: 'POST',
    body: JSON.stringify({
      client_adress: adress
    }),
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
    if(data.message=='Logged out. Please login and update token') {
      location.replace("/login");
    }
    message = document.getElementById('message');
    if (message != null) {
      message.innerHTML = data.message;
      message.classList.add("message");
      setTimeout( () => location.replace("/order") ,2000);
    }
    res = data.message;
  }).then(message => res)
}

cancel = () => {
  return fetch('/v2/users/cart_cancel', {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {

    message = document.getElementById('message');
    if (message != null) {
      message.innerHTML = data.message;
      message.classList.add("message");
      setTimeout( () => location.replace("/order") ,2000);
    }
    res = data.message;
  }).then(message => res)
}
