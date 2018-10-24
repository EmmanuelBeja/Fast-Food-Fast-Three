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

admin_menu = () => {
  //fetch menu
  return fetch('/v2/menu')
  .then(response => response.json())
  .then(data => {
    foods = data.Foods
    fooditem = document.getElementById('food-data');
    if (fooditem != null) {
      foods.forEach(food => {
        fooditem.innerHTML += '<div class="list-item"><div class="box-col-2"><img src="static/img/'+food.food_image+'" class="order-image"  alt=""></div><div class="box-col-6 order-description" >'+food.food_name+' | Price: Ksh.'+food.food_price+'<div class="box-col-8"><a href="javascript:;" id="'+food.food_id+'" onclick="edit_food(this.id)" class="btn-lightblue btn-small" name="button"> Edit</a><button type="button" id="'+food.food_id+'" onclick="delete_food(this.id)" class="btn-maroon btn-small" name="button"> Delete</button></div></div></div>';
      });
    }
    stat = data.status;
  }).then(status => stat);
}

//add food
addfood = (food_name, food_price, food_image) => {
  if (food_name == undefined) {
    food_name = document.getElementById('food_name').value;
    food_price = document.getElementById('food_price').value;
    food_image = food_name+'.jpg';
  }
  return fetch('/v2/menu', {
    method: 'POST',
    body: JSON.stringify({
      food_name: food_name,
      food_price: food_price,
      food_image: food_image
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
      setTimeout( () => location.replace("/a-food") ,3000);
    }
    res = data.message;
  }).then(message => res)
}

//redirect to page for editing
edit_food = food_id => {
  window.sessionStorage.setItem('food_id', food_id);
  location.replace("/a-edit-food");
}

//delete food
delete_food = food_id => {
  return fetch('/v2/food/'+food_id, {
    method: 'DELETE',
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
      setTimeout( () => location.replace("/a-food") ,3000);
    }
    stat = data.status;
  }).then(status => stat);
}
//Ok
