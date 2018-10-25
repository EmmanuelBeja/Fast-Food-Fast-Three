is_logged_in = () => {
 //check if token was created/ user is logged in
 if(!window.sessionStorage.getItem('token')){
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


editprofile = (username, userphone, password,  confirmpass) => {
  if (username == undefined) {
    username = document.getElementById('username').value;
    userphone = document.getElementById('userphone').value;
    password = document.getElementById('password').value;
    confirmpass = document.getElementById('confirmpass').value;
  }

  return fetch('/v2/users', {
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
    if (message != null) {
      message.innerHTML = data.message;
      message.classList.add("message");
      setTimeout( () => location.replace("/profile") ,3000);
    }
    res = data.message;
  }).then(message => res)
}
