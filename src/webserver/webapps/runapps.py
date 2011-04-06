'''
Created on 2 Sep 2010

@author: hshin
'''

import cherrypy
from forms.form import HTMLForms
#from actions.mriw import ReadMriwXML

from os import path

from lib import template

class WebappsForm(object):
            
    @cherrypy.expose
    @template.output('webapps.html')
    def index(self):
      return template.render()
    