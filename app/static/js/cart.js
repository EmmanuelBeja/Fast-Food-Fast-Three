is_logged_in = () => {
 //check role
 if( sessionStorage.getItem('token')!= null){
   let token = sessionStorage.getItem('token');
   return token;
 }else {
   location.replace('/')
 }
}

cart = token => {
  //fetch cart quantity and totalprice
  if (token == undefined ) {
    token = is_logged_in();
  }
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
