is_admin_logged_in = () => {
 //check if token was created & user is admin
 if(!window.sessionStorage.getItem('token')){
   return "not logged in";
   location.replace("/");
 }else {
   //check role
   userrole = window.sessionStorage.getItem('userrole');
   if (userrole!='admin') {
     location.replace("/menu");
   }
   token = window.sessionStorage.getItem('token');
   return "logged in";
 }
}

all_orders = () => {
  //fetch cart details
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
        orderdata.innerHTML += '<div class="list-item"><div class="box-col-8"><b>'+orderitem.food_name+'</b> | Price: Ksh.'+orderitem.food_price+' | Qty: '+orderitem.quantity+' | Status: '+orderitem.status+' | Date: '+orderitem.createddate+'<div class="box-col-8"><img src="static/img/location.png" class="location-icon" alt="">'+orderitem.client_adress+'. | Phone : '+orderitem.client_phone+' | By<i> '+orderitem.client_name+'</i>  <button type="button" class="btn-lightblue btn-small" id="'+orderitem.order_id+'" onclick="accepted(this.id)" name="button"> Accept</button><button type="button" class="btn-maroon btn-small" id="'+orderitem.order_id+'" onclick="declined(this.id)" name="button"> Decline</button><button type="button" class="btn-green btn-small" id="'+orderitem.order_id+'" onclick="completed(this.id)" name="button">Complete</button></div></div></div>';
      });
    }
    stat = data.status;
  }).then(status => stat);
}

accepted = order_id => {
  status = 'accepted';
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


declined = order_id => {
  status = 'declined';
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

completed = order_id => {
  status = 'completed';
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
