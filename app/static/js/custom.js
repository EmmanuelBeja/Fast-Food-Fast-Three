document.addEventListener("DOMContentLoaded", function() {
    var button = document.getElementById("submit");
    button.onclick = function(){
        var Username = document.getElementById("Username").value;
        var Password = document.getElementById("Password").value;

        p = {
            username:Username,
            password:Password
        }

        console.log(JSON.stringify(p))

        fetch('https://stackoverflowlitev3.herokuapp.com/api/v2/auth/login', {
        method: 'POST',
        mode: 'cors',
        redirect: 'follow',
        headers: new Headers({
        'Content-Type': 'application/json'
        }),
        body:JSON.stringify(p)
        }).then(function(response) {
        if (response.status == 201){
            response.json().then(data => {
                let token = (data.Access_token).substring(2, (data.Access_token).length -1);
                alert(token);
                window.sessionStorage.setItem('token', token);},
            window.location.replace("index.html"));
        }else if (response.status == 400 || response.status == 422){
            response.json().then(
                data =>
                { var arr = [];

                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        arr.push( [ key, data[key] ] );
                    }
                }alert(data[key]); window.location.reload(true);});
        }
        else{
        //failed
        response.json().then(data => console.log("Failed: ", data));
        }
        }).catch(err => console.log(err));
        function example(data){
            //execute some statements
            console.log(JSON.stringify(data));
        }
        return false;
    }
})
