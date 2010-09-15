
class HTMLForms():
  registerform = """
  <html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:py="http://rpacs.icr.ac.uk/">
  <head>
    <title>ROI-Engine: Registration Form</title>
  </head>
  <body class="register">
    <div id="header">
      <h1>Registration Form</h1>
    </div>


    <form action="register" method="post">
      <p>Username</p>
      <input type="text" name="username" value="" 
        size="15" maxlength="40"/>
    
      <p>Password</p>
      <input type="password" name="password" value="" 
        size="10" maxlength="40"/>

      <p>Confirm Password</p>
      <input type="password" name="password_confirm" value="" 
        size="10" maxlength="40"/>

      <p>E-Mail</p>
      <input type="text" name="email" value="" 
        size="15" maxlength="40"/>

      <p>Institution</p>
      <input type="text" name="institution" value="" 
        size="15" maxlength="40"/>

      <p>Department</p>
      <input type="text" name="department" value="" 
        size="15" maxlength="40"/>
    
      <p><input type="submit" value="Login"/></p>
      <p><input type="reset" value="Clear"/></p>
    </form>

    
    <div id="footer">
      <hr />
      <p class="legalese">ROI-Engine Copyright: 2010 Hoo Chang Shin</p>
    </div>
  </body>
  </html>
  """
  
  loginform = """
  <html xmlns="http://www.w3.org/1999/xhtml"
        xmlns:py="http://rpacs.icr.ac.uk/">
  <head>
    <title>ROI-Engine: Login Form</title>
  </head>
  <body class="login">
    <div id="header">
      <h1>Login Form</h1>
    </div>
      
    
    <form action="login" method="post">
      <p>Username</p>
      <input type="text" name="username" value="" size="10" maxlength="40"/>
      
      <p>Password</p>
      <input type="password" name="password" value="" size="10" maxlength="40"/>
        
      <p><input type="submit" value="Login"/></p>
      <p><input type="reset" value="Clear"/></p>
    </form>
    
    <div id="footer">
      <hr />
      <p class="legalese">ROI-Engine Copyright: 2010 Hoo Chang Shin</p>
    </div>
  </body>
  </html>
  """  
  
  
  webappsform = """
  <html xmlns="http://www.w3.org/1999/xhtml"
        xmlns:py="http://rpacs.icr.ac.uk/">
  <head>
    <title>ROI-Engine: Applications</title>
  </head>
  <body class="login">
    <div id="header">
      <h1>Applications</h1>
    </div>
      
    
    <form action="login" method="post">
      <p>Username</p>
      <input type="text" name="username" value="" size="10" maxlength="40"/>
      
      <p>Password</p>
      <input type="password" name="password" value="" size="10" maxlength="40"/>
        
      <p><input type="submit" value="Login"/></p>
      <p><input type="reset" value="Clear"/></p>
    </form>
    
    <div id="footer">
      <hr />
      <p class="legalese">ROI-Engine Copyright: 2010 Hoo Chang Shin</p>
    </div>
  </body>
  </html>
  """  
  
