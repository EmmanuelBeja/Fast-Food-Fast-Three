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

editing = () => {
  //check if user is really trying to edit a food item
  if(!window.sessionStorage.getItem('food_id')){
    location.replace("/a-home");
    return "not editing";
  }else {
    food_id = window.sessionStorage.getItem('food_id');
    return "editing"
  }
}

edited_food_details = food_id => {
  //fetch food we want to edit
  return fetch('/v2/food/'+food_id, {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
    foods = data.Foods
    fooditem = document.getElementById('food-data');
    if (fooditem != null) {
      fooditem.innerHTML += '<div class="list-item"><div class="box-col-2"><img src="static/img/'+foods.food_image+'" class="order-image"  alt=""></div><div class="box-col-6 order-description" >'+foods.food_name+' | Price: Ksh.'+foods.food_price+'</div></div>';
      document.getElementById('food_name').value += foods.food_name;
      document.getElementById('food_price').value += foods.food_price;
    }
    stat = data.status;
  }).then(status => stat);
}

editfood = (food_name, food_price, food_image, food_id) => {
  if (food_name == undefined) {
    food_name = document.getElementById('food_name').value;
    food_price = document.getElementById('food_price').value;
    food_image = food_name+'.jpg';
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
//Ok
