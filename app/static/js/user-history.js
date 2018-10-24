window.addEventListener('load', function () {
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
  fetch('/v2/users/orders', {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
    if(data.message=='Logged out. Please login and update token') {
      location.replace("/login");
    }
    orders = data.Orders
    i = 0;
    orders.forEach(function(order){
      let historydata = document.getElementById('historydata');
      historydata.innerHTML += '<div class="list-item"><div class="box-col-8">'+order.food_name+' | Price: Ksh.'+order.food_price+' | Qty: '+order.quantity+' Date: '+order.createddate+' | Status: <span class="'+order.status+'">'+order.status+'</span></div></div>';
      i++;
    });
  })
}, false);
