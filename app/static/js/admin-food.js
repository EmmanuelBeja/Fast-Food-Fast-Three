is_logged_in = () => {
 //check role
 if( sessionStorage.getItem('token')!= null){
   let token = sessionStorage.getItem('token');
   return token;
 }else {
   location.replace('/')
 }
}


admin_menu = token => {
  //fetch menu
  return fetch('/v2/menu')
  .then(response => response.json())
  .then(data => {
    foods = data.Foods
    fooditem = document.getElementById('food-data');
    if (fooditem != null) {
      foods.forEach(food => {
        fooditem.innerHTML += '<tr>'+
           '<td><img src="static/img/'+food.food_image+'" class="order-image"  alt=""></td>'+
           '<td>'+food.food_name+'</td>'+
           '<td>Ksh.'+food.food_price+'</td>'+
           '<td><a href="javascript:;" id="'+food.food_id+'" onclick="edit_food(this.id)" class="btn-lightblue btn-small" name="button"> Edit</a><button type="button" id="'+food.food_id+'" onclick="delete_food(this.id)" class="btn-maroon btn-small" name="button"> Delete</button></td>'+
           '</tr>';
      });
    }
    stat = data.status;
  }).then(status => stat);
}

//add food
addfood = (food_name, food_price, food_image, token) => {
  if (food_name == undefined || food_name == " ") {
    food_name = document.getElementById('food_name').value;
    food_price = document.getElementById('food_price').value;
    food_image = food_name+'.jpg';
    token = is_logged_in();
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
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+ token }
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
delete_food = (food_id, token) => {
  if (token == undefined ) {
    token = is_logged_in();
  }
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
