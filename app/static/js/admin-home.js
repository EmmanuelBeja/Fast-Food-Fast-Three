//check if token was created/ user is logged in
if(!window.sessionStorage.getItem('token')){
  location.replace("/");
}else {
  //check role
  userrole = window.sessionStorage.getItem('userrole');
  if (userrole!='admin') {
    location.replace("/menu");
  }
  token = window.sessionStorage.getItem('token');
}

//fetch cart details
fetch('/v2/orders/', {
  mode: 'cors',
  crossdomain: true,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
})
.then(response => response.json())
.then(data => {
  order = data.Orders
  orderdata = document.getElementById('orderdata');
  order.forEach(function(orderitem){
    orderdata.innerHTML += '<div class="list-item"><div class="box-col-8"><b>'+orderitem.food_name+'</b> | Price: Ksh.'+orderitem.food_price+' | Qty: '+orderitem.quantity+' | Status: '+orderitem.status+' | Date: '+orderitem.createddate+'<div class="box-col-8"><img src="static/img/location.png" class="location-icon" alt="">'+orderitem.client_adress+'. | Phone : '+orderitem.client_phone+' | By<i> '+orderitem.client_name+'</i>  <button type="button" class="btn-lightblue btn-small" id="'+orderitem.order_id+'" onclick="accepted(this.id)" name="button"> Accept</button><button type="button" class="btn-maroon btn-small" id="'+orderitem.order_id+'" onclick="declined(this.id)" name="button"> Decline</button><button type="button" class="btn-green btn-small" id="'+orderitem.order_id+'" onclick="completed(this.id)" name="button">Complete</button></div></div></div>';
  });
})

  accepted = order_id => {
    status = 'accepted';
    url = '/v2/orders/'+order_id
    fetch(url, {
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
     window.location.replace("/a-home");
    });
  }

  declined = order_id => {
    status = 'declined';
    url = '/v2/orders/'+order_id
    fetch(url, {
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
     window.location.replace("/a-home");
    });
  }

  completed = order_id => {
    status = 'completed';
    url = '/v2/orders/'+order_id
    fetch(url, {
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
     window.location.replace("/a-home");
    });
  }
