login = () => {
  username = document.getElementById('username').value;
  password = document.getElementById('password').value;

  fetch('/v2/auth/login', {
    method: 'POST',
    body: JSON.stringify({
      username: username,
      password: password
    }),
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8'}
  })
  .then(response => response.json())
  .then(data => {
    message = document.getElementById('message');
    message.innerHTML = data.message;

    token = data.token;
    window.sessionStorage.setItem('token', token);

    userrole = data.userrole;
    window.sessionStorage.setItem('userrole', userrole);

    redirect = () => {
      if(data.message=='You are successfully logged in') {
        if(userrole=='admin'){
          location.replace("/a-home");
        }else{
          location.replace("/menu");
        }
       }
    }

    setTimeout( redirect,1000);
  })
}
