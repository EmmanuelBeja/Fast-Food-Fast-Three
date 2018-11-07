is_logged_in = () => {
 //check role
 if( sessionStorage.getItem('token')!= null){
   let token = sessionStorage.getItem('token');
   return token;
 }else {
   location.replace('/')
 }
}

order_history = token => {
  //fetch user orders history
  if (token == undefined ) {
    token = is_logged_in();
  }
  return fetch('/v2/users/orders', {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
    if(data.message=='Logged out. Please login and update token') {
      location.replace("/login");
    }
    orders = data.Orders;
    console.log('orders');
    console.log(orders);
    const historydata = document.getElementById('historydata');
    if (historydata != null) {
      orders.forEach(function(order){
        historydata.innerHTML += '<tr>'+
           '<td>'+order.food_name+'</td>'+
           '<td>Ksh.'+order.food_price+'</td>'+
           '<td>'+order.quantity+'</td>'+
           '<td>'+order.createddate+'</td>'+
           '<td class="'+order.status+'">'+order.status+'</td>'+
         '</tr>';
      });

    }

    stat = data.status;
  }).then(status => stat)
}
