#!/usr/bin/env python
#
##
## Web Server
## Hoo Chang Shin
## E-Mail: hoo.shin@icr.ac.uk
##
#



import cherrypy
from genshi.template import TemplateLoader
from genshi.filters import HTMLFormFiller

from lib import template
from user_management.register import RegisterForm
from user_management.login import LoginForm

from webapps.runapps import WebappsForm
from actions.show_roi import ShowROI
from actions.show_roi import Download as show_roi_download

from cherrypy.lib.static import serve_file
  
import socket
import os

#from mainpage import *


class Root(object):
    
  registerForm = RegisterForm()
  loginForm = LoginForm()
  
  webappsForm = WebappsForm()
  
  showROI = ShowROI()
  showROI.download = show_roi_download()
  
    
  @cherrypy.expose
  #@template.output('index.html') IGNORE THE LOGIN FOR NOW
  @template.output('mainPage.html')
  def index(self):
    return template.render()


#os.system('/Users/hshin/SoftwareDev/apache-tomcat-7.0.11/bin/startup.sh')  
# IGNORE THE DOCUMENTATION SERVER FOR NOW  


current_path = os.getcwd()
upper_upper_path = os.path.dirname(os.path.dirname(current_path))
data_path = os.path.join(upper_upper_path, 'data', 'image')
print data_path

local_ip_address = socket.gethostbyname(socket.gethostname())
cherrypy.config.update({'server.socket_host': local_ip_address,
                        'server.socket_port': 9090,
                       })

conf = {'/image':
        {'tools.staticdir.on':True,
         'tools.staticdir.dir':
         data_path}}

cherrypy.server.max_request_body_size = 0
cherrypy.server.socket_timeout = 60

cherrypy.quickstart(Root(), '/', config=conf)

