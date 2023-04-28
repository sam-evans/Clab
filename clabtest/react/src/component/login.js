import React from 'react';
  
function Login () {
    return  <div className="login-form">
    <h1>Log In</h1>
<form action="/login" method = "POST">
    <p>Username <input id="username" type = "text" name = "username" placeholder="username"/></p>
    <p>Password <input id="password" type = "password" name = "password" placeholder="password"/></p>
<p><input className="button-19" id="submit" type = "submit" value = "Log In" /></p>
</form>
<div className="controls">
<p id="response"></p>
</div>
</div>

}
export default Login;

