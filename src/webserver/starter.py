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
  
import socket

from mainpage import *


class Root(object):

  registerForm = RegisterForm()
  loginForm = LoginForm()
    
    
  @cherrypy.expose
  @template.output('index.html')
  def index(self):      
    return template.render()
  
  
local_ip_address = socket.gethostbyname(socket.gethostname())
cherrypy.config.update({#'server.socket_host': local_ip_address,
                        'server.socket_host': '127.0.0.1',
                        #'server.socket_host': '172.16.15.156', # ICR
                        'server.socket_port': 9090,
                       })

cherrypy.quickstart(Root())

