import os
import datetime
import urllib
from google.appengine.ext import db
from google.appengine.api import users

import os
import datetime
import urllib
from google.appengine.ext import db
from google.appengine.api import users

class Hub(db.Model):
    name = db.StringProperty(required=False)
    location = db.StringProperty(required=False)
    password_hash = db.StringProperty(required=False)
    websites_list = db.StringListProperty(required=True)
    phone_numbers = db.StringListProperty(required=True)
    twitter_list = db.StringListProperty(required=True)

class Resource(db.Model):
    name = db.StringProperty(required=False)
    location = db.StringProperty(required=False) 
    notes = db.StringProperty(required=False)
    priority_level = db.StringProperty(required=False)
    

class Need(db.Model):
    name = db.StringProperty(required=False)
    location = db.StringProperty(required=False)
    notes = db.StringProperty(required=False)
    priority_level = db.StringProperty(required=False)
    
class Volunteer(db.Model):
    name = db.StringProperty(required=False)
    category = db.StringProperty(required=False)
    email = db.StringProperty(required=False)
    phone = db.StringProperty(required=False)
    preferred_locations = db.StringListProperty(required=True)
    activated_locations = db.StringListProperty(required=True)
    availability = db.StringListProperty(required=True)
    available_now = db.StringListProperty(required=True)
    notes = db.StringProperty(required=False)
    
class Car(db.Model):
    name = db.StringProperty(required=False)
    preferred_locations = db.StringListProperty(required=True)
    activated_locations = db.StringListProperty(required=True)
    phone_numbers = db.StringProperty(required=False)
    notes = db.StringProperty(required=False)
    
    

class CanvassSheets(db.Model):
    volunteer_name = db.StringProperty(required=False)
    location = db.StringProperty(required=False)
    people_names = db.StringListProperty(required=True)
    need_scale = db.StringProperty(required=False)
    needs = db.StringProperty(required=False)
    notess = db.StringProperty(required=False)
    
