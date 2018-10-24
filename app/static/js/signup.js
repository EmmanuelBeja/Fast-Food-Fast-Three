signup = (username, userphone, password,  confirmpass) => {
  //sign up
  if (username == undefined|| password == undefined) {
    username = document.getElementById('username').value;
    userphone = document.getElementById('userphone').value;
    password = document.getElementById('password').value;
    confirmpass = document.getElementById('confirmpass').value;
  }

  return fetch('http://127.0.0.1:5000/v2/auth/signup', {
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
    const message = document.getElementById('message');
    if (message != null) {
      message.innerHTML = data.message;
      message.classList.add("message");
    }

    res = data.message;
  }).then(message => res)

}
