
from datetime import datetime

class Link(object):

  def __init__(self, username, password, department):
    self.username = username
    self.password = password
    self.department = department
    self.time = datetime.utcnow()
    self.id = hex(hash(tuple([username, password, department, self.time])))[2:]
    self.comments = []

    def __repr__(self):
      return '<%s %r>' % (type(self).__name__, self.title)

  def add_comment(self, username, content):
    comment = Comment(username, content)
    self.comments.append(comment)
    return comment


class Comment(object):

  def __init__(self, username, content):
    self.username = username
    self.content = content
    self.time = datetime.utcnow()

  def __repr__(self):
    return '<%s by %r>' % (type(self).__name__, self.username)
