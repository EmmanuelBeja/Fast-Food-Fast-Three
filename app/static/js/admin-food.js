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

//fetch menu
fetch('/v2/menu')
.then(response => response.json())
.then(data => {
  foods = data.Foods
  fooditem = document.getElementById('food-data');
  foods.forEach(food => {
    fooditem.innerHTML += '<div class="list-item"><div class="box-col-2"><img src="static/img/'+food.food_image+'" class="order-image"  alt=""></div><div class="box-col-6 order-description" >'+food.food_name+' | Price: Ksh.'+food.food_price+'<div class="box-col-8"><a href="javascript:;" id="'+food.food_id+'" onclick="edit_food(this.id)" class="btn-lightblue btn-small" name="button"> Edit</a><button type="button" id="'+food.food_id+'" onclick="delete_food(this.id)" class="btn-maroon btn-small" name="button"> Delete</button></div></div></div>';
  });
})

//add food
addfood = () => {
  food_name = document.getElementById('food_name').value;
  food_price = document.getElementById('food_price').value;
  food_image = food_name+'.jpg';

  fetch('/v2/menu', {
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
    message.innerHTML = data.message;
  })
}



//redirect to page for editing
edit_food = food_id => {
  window.sessionStorage.setItem('food_id', food_id);
  location.replace("/a-edit-food");
}

//delete food
delete_food = food_id => {
  url = '/v2/food/'+food_id
  fetch(url, {
    method: 'DELETE',
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token}
  })
  .then(response => response.json())
  .then(data => {
    console.log(data)
    location.replace("/a-food")
  })
}
