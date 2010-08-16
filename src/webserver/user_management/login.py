

import cherrypy
from forms.form import HTMLForms

from os import path

from bsddb3.db import *
from dbxml import *

from lib import template

class LoginForm(object):
  
  @cherrypy.expose
  def index(self):
    forms = HTMLForms()
    return forms.loginform
  
  @cherrypy.expose
  @template.output('mainpage.html')
  def login(self, username=None, password=None):
    
    user_db = path.join('..', '..', 'db', 'users.dbxml')
    # for test purpose
    #user_db = path.join('..', '..', '..', 'db', 'users.dbxml')
    
    if not path.exists(user_db):
      return 'Error loading the ROI-Engine database.'
    else:
      pass
    
    mgr = XmlManager()
    container = mgr.openContainer(user_db)
    xmlucontext = mgr.createUpdateContext()
    
    users_query = "collection()/" + username + '[@password=' + \
                  '"' + password + '"]'
    xmlqcontext = mgr.createQueryContext()
    
    xmlqcontext.setDefaultCollection(user_db)
    queryexp = mgr.prepare(users_query, xmlqcontext)
    results = queryexp.execute(xmlqcontext)
    
    name = 0
    try:
      for value in results:
        document = value.asDocument()
        name = document.getName()
        content = value.asString()
    except Error:
      pass
    
    if name is not 0:
      print 'Login successful.'
      
      del container
      return template.render()
      #return 'file://localhost/Users/hshin/workspace/ROI-Engine/doc/sphinx/' + \
      #       'build/html/index.html'
    
    else:
      print 'Username not found or password does not match.'
      return 'Username not found or password does not match.'
  
    
  

if __name__=="__main__":
  loginform = LoginForm()
  loginform.login('hshin', 'hshin')
  
  