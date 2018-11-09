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

//searchfood
searchfood = token => {
  if (token == undefined ) {
    token = is_logged_in();
  }

    searchedfood = document.getElementById("search-input").value;
    console.log(searchedfood);
    if (searchedfood.length > 0) {
      message.style.display = "block";
      searchResult.style.display = "none";
      message.innerHTML = searchedfood+' not available.';
      message.classList.add("search-message");
      searchloader = document.getElementById("search-loader");
      searchloader.style.display = "block";

      return fetch('/v2/menu')
      .then(response => response.json())
      .then(data => {
        let foods = data.Foods;
        let searchResult = document.getElementById('searchResult');
        let message = document.getElementById('message');
        if (searchResult != null) {
          foods.find(food => {
           if (food.food_name == searchedfood) {
             //print the food name and image and price
             //searchedfood.classList.add("search-input-success");
             searchResult.style.display = "block";

             searchResult.innerHTML = '<div class="box-col-8 searchresult"><table id="table"><tr>'+
                '<td><img src="static/img/'+food.food_image+'" class="order-image"  alt=""></td>'+
                '<td>'+food.food_name+'</td>'+
                '<td>Ksh.'+food.food_price+'</td>'+
                '<td><a href="javascript:;" id="'+food.food_id+'" onclick="pick_food(this.id)" class="btn-brown btn-large btn-wide">Add to Cart.<img src="static/img/add.png" class="food-add-icon" style="height:20px;width:20px;" alt=""></a></td>'+
                '</tr></table></div>';

              searchloader.style.display = "none";
              message.style.display = "none";

          // } else {
          //   message.style.display = "block";
          //   //searchResult.style.display = "none";
          //   message.innerHTML = searchedfood+' not available.';
          //   message.classList.add("search-message");
           }
          })
        }
      })
    } else {
      //message.style.display = "none";
      searchResult.style.display = "none";
      message.style.display = "none";
      searchloader.style.display = "none";
    }

}
