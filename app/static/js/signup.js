signup = () => {
  username = document.getElementById('username').value;
  userphone = document.getElementById('userphone').value;
  password = document.getElementById('password').value;
  confirmpass = document.getElementById('confirmpass').value;

  fetch('/v2/auth/signup', {
    method: 'POST',
    body: JSON.stringify({
      username: username,
      userphone: userphone,
      password: password,
      confirmpass: confirmpass
    }),
    mode: 'cors',
    crossdomain: true,
    headers: { 'Content-Type': 'application/json; charset=utf-8'}
  })
  .then(response => response.json())
  .then(data => {
    message = document.getElementById('message');
    message.innerHTML = data.message;
  })
}
