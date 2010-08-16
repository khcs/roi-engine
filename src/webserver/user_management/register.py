

import cherrypy
from forms.form import HTMLForms

from os import path

from bsddb3.db import *
from dbxml import *

from lxml import etree
from xml.dom.minidom import Document, parse, parseString


class RegisterForm(object):

  @cherrypy.expose
  def index(self):
    forms = HTMLForms()
    return forms.registerform


  @cherrypy.expose
  def register(self, username=None, password=None, password_confirm=None, \
               email=None, institution=None, department=None):


    if password != password_confirm:
      return 'Passwords do not match! Go backward and fill them again!'

    elif not('@' in email) or not('.' in email):
      return 'You bastard! You entered a fake E-mail address!\n' + \
             'Go backward and fill it again!'

 
    user_db = path.join('..', '..', 'db', 'users.dbxml')
    # for test purpose
    #user_db = path.join('..', '..', '..', 'db', 'users.dbxml')
    
    mgr = XmlManager()
    
    if not path.exists(user_db):
      try:
        container = mgr.createContainer(user_db)
        xmlucontext = mgr.createUpdateContext()
      except IOError as (errno, strerror):
        return 'An error occured in ROI-Eninge during registration: ' \
                + 'I/O error({0}): {1}'.format(errno, strerror)
    else:
      try:
        container = mgr.openContainer(user_db)
        xmlucontext = mgr.createUpdateContext()
      except XmlException, inst:
        print 'XmlException (', inst.exceptionCode, '): ', inst.what
        if inst.exceptionCode == DATABASE_ERROR:
          print "Database error code:", inst.dbError
          
    users_query = "collection()/" + username 
    #"collection(" + user_db + ")/" + username   
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
        #print name, ": ", content
    except UnboundLocalError:
      pass

    if name is not 0:
      print 'User exists'
      return 'Username already exists!'
    else:
      print 'User does not exist. Created the database for the new user.'
      new_user_xml = self.register_new_user_dom_way(username, password, email,\
                                                    institution, department)    
      container.putDocument(username, new_user_xml.toxml(), xmlucontext)
      
      del container      
      return 'New user database successfully created!\n', \
             'You can either go back to the main page to login,\n', \
             'or use the ROI-Engine from your local client.'
    

  def register_new_user_dom_way(self, username, password, email, institution, \
                        department):
    new_user_document = Document()
    
    new_user_element = new_user_document.createElement(username)
    new_user_element.setAttribute("username", username)
    new_user_element.setAttribute("password", password)
    new_user_element.setAttribute("email", email)
    new_user_element.setAttribute("institution", institution)
    new_user_element.setAttribute("department", department)
    
    new_user_document.appendChild(new_user_element)    
        
    return new_user_document
  
  
  
  
  
  
  def xml_test(self):
    xml_d = self.register_new_user_dom_way('USER', 'PSWD', 'EMAIL', 'INST', 'DPMT')
    #xml_d = etree.parse(xml_e)
    #print xml_d.toprettyxml(indent="  ")
    print xml_d.toxml()

if __name__=="__main__":
   registerForm = RegisterForm()
   #registerForm.xml_test()
   registerForm.register('hshin', 'ab', 'ab', 'hugeiezzy@gmail.com', 'ICR', 'CLINMAG')
   