//check if token was created/ user is logged in
if(!window.sessionStorage.getItem('token')){
  location.replace("/");
}else {
  token = window.sessionStorage.getItem('token');
}

//fetch cart quantity and totalprice
cart = () => {
  fetch('/v2/users/cart_quantity', {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
    let cart_quantity = document.getElementById('cart');
    cart_quantity.innerHTML = data.Cart
    let cart_total_price = document.getElementById('cart_total_price');
    cart_total_price.innerHTML = data.totalprice
  })
}

cart();

//fetch cart details
fetch('/v2/users/cart', {
  mode: 'cors',
  crossdomain: true,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
})
.then(response => response.json())
.then(data => {
  cart = data.Cart
  cartdata = document.getElementById('cartdata');
  cart.forEach(function(cartitem){
    cartdata.innerHTML += '<div class="list-item"><div class="box-col-8">'+cartitem.food_name+' | Price: Ksh.'+cartitem.price+' | Qty: '+cartitem.quantity+'</div></div>';
  });
  cartdata.innerHTML +='<div class="list-item"><div class="box-col-8">Total: Ksh. '+data.totalprice+'</div></div>'
})

//place order function
order = () => {
  adress = document.getElementById('adress').value;

  fetch('/v2/users/orders', {
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
    message.innerHTML = data.message;
  })
}

cancel = () => {
  fetch('/v2/users/cart_cancel', {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
    window.location.replace("/order");
  })
}
