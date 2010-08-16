#!/usr/bin/env python


import operator, os, pickle, sys

import cherrypy
from formencode import Invalid
from genshi.template import TemplateLoader
from genshi.filters import HTMLFormFiller

from form import *
from model import Link, Comment
from lib import template


class Root():

  def __init__(self):
    a = 1
    #self.data = data

  @cherrypy.expose
  @template.output('index.html')
  def index(self):
    #links = sorted(self.data.values(), key=operator.attrgetter('time'))
    links = ['a1', 'b2']    
    return template.render(links=links)

  @cherrypy.expose
  @template.output('registration.html')
  def register(self, cancel=False):
    if cherrypy.request.method == 'POST':
      if cancel:
        raise cherrypy.HTTPRedirect('/')
      form = RegistrationForm()

      try:
        print username
        """
        data = form.to_python(data)
        link = Link(**data)
        self.data[link.id] = link
        raise cherrypy.HTTPRedirect('/')
        """
      except Invalid, e:
        errors = e.unpack_errors()
        
    else:
      errors = {}
            
    return template.render(errors=errors) | HTMLFormFiller(data=form.username)
  


def main():

  """
  # load data from the pickle file, or initialize it to an empty list
  if os.path.exists(filename):
    fileobj = open(filename, 'rb')
    try:
      data = pickle.load(fileobj)
    finally:
      fileobj.close()

    def _save_data():
      # save data back to the pickle file
      fileobj = open(filename, 'wb')
      try:
        pickle.dump(data, fileobj)
      finally:
        fileobj.close()

    if hasattr(cherrypy.engine, 'subscribe'):
      cherrypy.engine.subscribe('stop', _save_data)
    else:
      cherrypy.engine.on_stop_engine_list.append(_save_data)
  """    

  # Some global configuration; note that this could be moved into a
  # configuration file
  cherrypy.config.update({
    'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
    'tools.decode.on': True,
    'tools.trailing_slash.on': True,
    'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
  })

  cherrypy.quickstart(Root(), '/', {
    '/media': {
      'tools.staticdir.on': True,
      'tools.staticdir.dir': 'static'
    }
  })


if __name__ == '__main__':
    main()

