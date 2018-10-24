//check if token was created/ user is logged in
if(!window.sessionStorage.getItem('token')){
  location.replace("/");
}else {
  token = window.sessionStorage.getItem('token');
}

//fetch cart quantity and totalprice
cart = () => {
  fetch('/v2/users/cart_quantity', {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
    let cart_quantity = document.getElementById('cart');
    cart_quantity.innerHTML = data.Cart
    let cart_total_price = document.getElementById('cart_total_price');
    cart_total_price.innerHTML = data.totalprice
  })
}

cart();

  //fetch menu
  fetch('/v2/menu')
  .then(response => response.json())
  .then(data => {
    foods = data.Foods
    fooditem = document.getElementById('food-data');
    foods.forEach(function(food){
      fooditem.innerHTML += '<div class="box-col-2"><div class="food-panel"><img src="static/img/'+food.food_image+'" '+
      'class="food-image" alt=""><div class="food-panel-content"><div class="food-title text-fit">'+food.food_name+'</div>'+
      '<div class="food-description"><span class="price text-fit">Ksh.'+food.food_price+'</span><span class="span-add-to-cart">'+
      '<a href="javascript:;" id="'+food.food_id+'" onclick="pick_food(this.id)" class="btn-brown btn-large btn-wide">Add to Cart.<img src="static/img/add.png" class="food-add-icon" '+
      'style="height:20px;width:20px;" alt=""></a></span></div></div><div></div>';
    });
  })

  //add to cart
  pick_food = food_id => {
    let url = '/v2/users/pick_food/'+food_id;
    fetch(url, {
      mode: 'cors',
      crossdomain: true,
      headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
    })
    .then(response => response.json())
    .then(data => {
     window.location.replace("/menu");
    });

  };
