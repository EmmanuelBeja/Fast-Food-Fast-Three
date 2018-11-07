is_logged_in = () => {
 //check role
 if( sessionStorage.getItem('token')!= null){
   let token = sessionStorage.getItem('token');
   return token;
 }else {
   location.replace('/')
 }
}


editprofile = (username, userphone, password,  confirmpass, token) => {
  if (username == undefined) {
    username = document.getElementById('username').value;
    userphone = document.getElementById('userphone').value;
    password = document.getElementById('password').value;
    confirmpass = document.getElementById('confirmpass').value;
    token = is_logged_in();
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
      setTimeout( () => location.reload() ,3000);
    }
    res = data.message;
  }).then(message => res)
}
