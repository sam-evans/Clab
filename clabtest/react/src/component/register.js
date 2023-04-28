import React from 'react';
  
function Register () {
    return     <div className="register-form">
    <h1>Sign up for clab</h1>
<form action="/register" method = "POST">
    <p>Email <input id="email" type = "text" name = "email" placeholder="email"/></p>
    <p>Username <input id="username" type = "text" name = "username" placeholder="username"/></p>
    <p>Password <input id="password" type = "password" name = "password" placeholder="password"/></p>
<p><input className="button-19" id="submit" type = "submit" value = "Register" /></p>
</form>
<div className="controls">
<p id="response"></p>
</div>
<form action="/login" class="inline">
    <button class="float-left submit-button" >Already registered? Log in here</button>
</form>
</div>
}
export default Register;