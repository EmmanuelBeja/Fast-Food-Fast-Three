is_logged_in = () => {
 //check role
 if( sessionStorage.getItem('token')!= null){
   let token = sessionStorage.getItem('token');
   return token;
 }else {
   location.replace('/')
 }
}


all_orders = token => {
  //fetch cart details
  if (token == undefined ) {
    token = is_logged_in();
  }
  return fetch('/v2/orders/', {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
    order = data.Orders
    orderdata = document.getElementById('orderdata');
    if (orderdata != null) {
      order.forEach(function(orderitem){
        orderdata.innerHTML += '<tr>'+
           '<td>'+orderitem.client_name+'</td>'+
           '<td>'+orderitem.client_phone+'</td>'+
           '<td><img src="static/img/location.png" class="location-icon" alt="">'+orderitem.client_adress+'</td>'+
           '<td>'+orderitem.food_name+'</td>'+
           '<td>Ksh.'+orderitem.food_price+'</td>'+
           '<td>'+orderitem.quantity+'</td>'+
           '<td>'+orderitem.createddate+'</td>'+
           '<td>'+orderitem.status+'</td>'+
           '<td><button type="button" class="btn-lightblue btn-small" id="'+orderitem.order_id+'" onclick="accepted(this.id)" name="button"> Accept</button>'+
           '<button type="button" class="btn-maroon btn-small" id="'+orderitem.order_id+'" onclick="declined(this.id)" name="button"> Decline</button>'+
           '<button type="button" class="btn-green btn-small" id="'+orderitem.order_id+'" onclick="completed(this.id)" name="button">Complete</button></td>'+
         '</tr>';
      });
    }
    stat = data.status;
  }).then(status => stat);
}

accepted = (order_id, token) => {
  status = 'accepted';
  if (token == undefined ) {
    token = is_logged_in();
  }
  return fetch('/v2/orders/'+order_id, {
    method: 'PUT',
    body: JSON.stringify({
      status: status
    }),
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
      setTimeout( () => location.replace("/a-home") ,2000);
    }
   res = data.message;
 }).then(message => res)
}


declined = (order_id, token) => {
  status = 'declined';
  if (token == undefined ) {
    token = is_logged_in();
  }
  return fetch('/v2/orders/'+order_id, {
    method: 'PUT',
    body: JSON.stringify({
      status: status
    }),
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
      setTimeout( () => location.replace("/a-home") ,2000);
    }
    res = data.message;
  }).then(message => res)
}

completed = (order_id, token) => {
  status = 'completed';
  if (token == undefined ) {
    token = is_logged_in();
  }
  return fetch('/v2/orders/'+order_id, {
    method: 'PUT',
    body: JSON.stringify({
      status: status
    }),
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
      setTimeout( () => location.replace("/a-home") ,2000);
    }
    res = data.message;
  }).then(message => res)
}
