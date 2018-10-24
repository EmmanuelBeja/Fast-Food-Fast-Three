login = (username, password) => {
  //login
  if (username == undefined) {
    username = document.getElementById('username').value;
    password = document.getElementById('password').value;
  }

  return fetch('http://127.0.0.1:5000/v2/auth/login', {
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
    const message = document.getElementById('message');
    if (message != null) {
      message.innerHTML = data.message;
      message.classList.add("message");
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
    }

    const token = data.token;
    window.sessionStorage.setItem('token', token);
    const userrole = data.userrole;
    window.sessionStorage.setItem('userrole', userrole);

    res = data.message;
  }).then(message => res)
}
