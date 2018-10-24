menu = () => {
  //fetch menu
  return fetch('/v2/menu')
  .then(response => response.json())
  .then(data => {
    foods = data.Foods;
    fooditem = document.getElementById('food-data');
    if (fooditem != null) {
      foods.forEach(function(food){
        fooditem.innerHTML += '<div class="box-col-2"><div class="food-panel"><img src="static/img/'+food.food_image+'" '+
        'class="food-image" alt=""><div class="food-panel-content"><div class="food-title text-fit">'+food.food_name+'</div>'+
        '<div class="food-description"><span class="price text-fit">Ksh.'+food.food_price+'</span><span class="span-add-to-cart">'+
        '<a href="/login" class="btn-brown btn-large btn-wide">Add to Cart.<img src="static/img/add.png" class="food-add-icon" '+
        'style="height:20px;width:20px;" alt=""></a></span></div></div><div></div>';
      });
    }
    stat = data.status;
  }).then(status => stat);
}
