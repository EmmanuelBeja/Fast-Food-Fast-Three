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


editprofile = (username, userphone, password,  confirmpass) => {
  if (username == undefined) {
    username = document.getElementById('username').value;
    userphone = document.getElementById('userphone').value;
    password = document.getElementById('password').value;
    confirmpass = document.getElementById('confirmpass').value;
  }

  return fetch('/v2/users', {
    method: 'PUT',
    body: JSON.stringify({
      username: username,
      userphone: userphone,
      password: password,
      confirmpass: confirmpass
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
      setTimeout( () => location.replace("/a-profile") ,3000);
    }
    res = data.message;
  }).then(message => res)
}