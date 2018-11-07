is_logged_in = () => {
 //check role
 if( sessionStorage.getItem('token')!= null){
   let token = sessionStorage.getItem('token');
   return token;
 }else {
   location.replace('/')
 }
}

menu = token => {
  //fetch menu
  if (token == undefined ) {
    token = is_logged_in();
  }
  return fetch('/v2/menu')
  .then(response => response.json())
  .then(data => {
    let foods = data.Foods;
    fooditem = document.getElementById('food-data');
    if (fooditem != null) {
      let i = 1;
      foods.forEach(function(food){
        //display first four
        if (i<=4) {
          fooditem.innerHTML += '<div class="box-col-2"><div class="food-panel"><img src="static/img/'+food.food_image+'" '+
        'class="food-image" alt=""><div class="food-panel-content"><div class="food-title text-fit">'+food.food_name+'</div>'+
        '<div class="food-description"><span class="price text-fit">Ksh.'+food.food_price+'</span><span class="span-add-to-cart">'+
        '<a href="javascript:;" id="'+food.food_id+'" onclick="pick_food(this.id)" class="btn-brown btn-large btn-wide">Add to Cart.<img src="static/img/add.png" class="food-add-icon" '+
        'style="height:20px;width:20px;" alt=""></a></span></div></div><div></div>';
        }
        i++;
      });
    }
    stat = data.status;
  }).then(status => stat);
}


pick_food = (food_id, token) => {
  //add to cart
  if (token == undefined ) {
    token = is_logged_in();
  }
  let url = '/v2/users/pick_food/'+food_id;
  return fetch(url, {
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer '+token }
  })
  .then(response => response.json())
  .then(data => {
   cart();
   stat = data.status;
 }).then(status => stat);
}




window.sessionStorage.setItem('index-counter', 3);
window.onscroll = function() {
  var d = document.documentElement;
  var offset = d.scrollTop + window.innerHeight;
  var height = d.offsetHeight;

  if (offset === height) {
    return fetch('/v2/menu')
    .then(response => response.json())
    .then(data => {
      let foods = data.Foods;
      let i = 0;
      let mincount = sessionStorage.getItem('index-counter');
      let maxcount = parseInt(mincount)+ 5;

      foods.forEach(food => {
        //check if last loop reached
        if (i > mincount && i < maxcount) {
          if (foods.length > i) {
            fooditem.innerHTML += '<div class="box-col-2"><div class="food-panel"><img src="static/img/'+food.food_image+'" '+
            'class="food-image" alt=""><div class="food-panel-content"><div class="food-title text-fit">'+food.food_name+'</div>'+
            '<div class="food-description"><span class="price text-fit">Ksh.'+food.food_price+'</span><span class="span-add-to-cart">'+
            '<a href="/login" class="btn-brown btn-large btn-wide">Add to Cart.<img src="static/img/add.png" class="food-add-icon" '+
            'style="height:20px;width:20px;" alt=""></a></span></div></div><div></div>';

            window.sessionStorage.setItem('index-counter', i);
          }
        }else if (parseInt(i)+1 == foods.length) {
          let loadMore = document.getElementById("loadMore");
          loadMore.style.display = "none";
        }
        i++;
      });

      stat = data.status;
    })
  }
};
