import React from 'react';
  
function Contact (){
 return     <div class="title-body">
 <h1>Contact Us!</h1>
 <p>Email <input id="email" type = "text" name = "email" placeholder="email"/></p>
 <p>Name <input id="username" type = "text" name = "username" placeholder="name"/></p>
 <p><textarea class="message" type = "text" name = "password" placeholder="Message..."></textarea></p>
<div class="controls" id="b1"><input class="button-19" id="submit" type = "submit"/></div>
</div>
}
  
export default Contact;