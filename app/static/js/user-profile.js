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

editprofile = () => {
  username = document.getElementById('username').value;
  userphone = document.getElementById('userphone').value;
  password = document.getElementById('password').value;
  confirmpass = document.getElementById('confirmpass').value;

  fetch('/v2/users', {
    method: 'PUT',
    body: JSON.stringify({
      username: username,
      userphone: userphone,
      password: password,
      confirmpass: confirmpass
    }),
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token}
  })
  .then(response => response.json())
  .then(data => {
    message = document.getElementById('message');
    message.innerHTML = data.message;
  })
}
