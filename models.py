from google.appengine.ext import ndb

class Employee(ndb.Model):
    name = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    dob = ndb.DateProperty()
    gender = ndb.StringProperty()
    hire_date = ndb.DateProperty()
    salary = ndb.FloatProperty()
    profile_image = ndb.StringProperty()
    department = ndb.StringProperty()

class Department(ndb.Model):
    name = ndb.StringProperty()
    code = ndb.StringProperty()