
import formencode
from formencode import Schema, validators


class RegistrationForm(Schema):
  username = validators.UnicodeString(validators.PlainText())#, UniqueUsername())
  password = validators.UnicodeString(not_empty=True)
  password_confirm = validators.String()
  email = validators.Email(not_empty=True)
  institution = validators.UnicodeString(not_empty=True)
  department = validators.UnicodeString(not_empty=True)
  #url = validators.URL(not_empty=True, add_http=True, check_exists=False)
  chained_validators = [validators.FieldsMatch('password', 'password_confirm')]
  

class CommentForm(Schema):
  username = validators.UnicodeString(not_empty=True)
  content = validators.UnicodeString(not_empty=True)


class UniqueUsername(formencode.FancyValidator):
  def _to_python(self, value, state):
    if value in usernames:
      raise formencode.Invalid('That username already exists', value, state)
    return value
 
