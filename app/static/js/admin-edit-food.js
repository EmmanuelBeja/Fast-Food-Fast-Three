is_logged_in = () => {
 //check role
 if( sessionStorage.getItem('token')!= null){
   let token = sessionStorage.getItem('token');
   return token;
 }else {
   location.replace('/')
 }
}


editing = () => {
  //check if user is really trying to edit a food item
  if(!window.sessionStorage.getItem('food_id')){
    location.replace("/a-home");
  }else {
    food_id = window.sessionStorage.getItem('food_id');
    return food_id;
  }
}

edited_food_details = (food_id, token) => {
  //fetch food we want to edit
  if (token == undefined ) {
    token = is_logged_in();
  }
  return fetch('/v2/food/'+food_id, {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
    food = data.Foods
    fooditem = document.getElementById('food-data');
    if (fooditem != null) {
      fooditem.innerHTML += '<tr>'+
         '<td><img src="static/img/'+food.food_image+'" class="order-image"  alt=""></td>'+
         '<td>'+food.food_name+'</td>'+
         '<td>Ksh.'+food.food_price+'</td>'+
         '</tr>';
      document.getElementById('food_name').value += food.food_name;
      document.getElementById('food_price').value += food.food_price;
    }
    stat = data.status;
  }).then(status => stat);
}

editfood = (food_name, food_price, food_image, food_id, token) => {
  if (food_name == undefined) {
    food_name = document.getElementById('food_name').value;
    food_price = document.getElementById('food_price').value;
    food_image = food_name+'.jpg';
    token = is_logged_in();
    food_id = editing();
  }
  return fetch('/v2/food/'+food_id, {
    method: 'PUT',
    body: JSON.stringify({
      food_name: food_name,
      food_price: food_price,
      food_image: food_image
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
      setTimeout( () => location.replace("/a-edit-food") ,3000);
    }
    stat = data.status;
  }).then(status => stat);
}
