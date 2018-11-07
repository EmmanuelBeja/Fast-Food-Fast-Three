is_logged_in = () => {
 //check role
 if( sessionStorage.getItem('token')!= null){
   let token = sessionStorage.getItem('token');
   return token;
 }else {
   location.replace('/')
 }
}

cart_details = token => {
  //fetch cart details
  if (token == undefined ) {
    token = is_logged_in();
  }
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
        cartdata.innerHTML += '<tr>'+
           '<td>'+cartitem.food_name+'</td>'+
           '<td>Ksh.'+cartitem.price+'</td>'+
           '<td>'+cartitem.quantity+'</td>'+
         '</tr>';
      });
      cartdata.innerHTML +='<div class="list-item"><div class="box-col-8">Total: Ksh. '+data.totalprice+'</div></div>'
    }
    res = data.message;
  }).then(message => res)
}


//place order function
order = (adress, token) => {
  if (adress == undefined) {
    adress = document.getElementById('adress').value;
    token = is_logged_in();
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

cancel = token => {
  if (token == undefined ) {
    token = is_logged_in();
  }
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
