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

class Member(db.Model):
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    category = db.StringProperty(required=True)
    first_name = db.StringProperty(required=False)
    last_name = db.StringProperty(required=False)
    twitter = db.StringProperty(required=False)
    orgs = db.StringProperty(required=False)
    anything_else = db.StringProperty(required=False)
    orgs_list = db.StringListProperty(required=True)
    location = db.StringProperty(required=False)
    rep_points = db.IntegerProperty(default=0)
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    
class Post(db.Model):
    post_id = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    tags = db.StringProperty(required=True)
    entry = db.TextProperty(required=True)
    tags_list = db.StringListProperty(required=True)
    timestamp = db.StringProperty(required=True)
    points = db.IntegerProperty(required=False)
    
    
class Tag(db.Model):
    tag = db.StringProperty(required=True)

class Comment(db.Model):
    comment = db.TextProperty(required=True)
    email = db.StringProperty(required=True)
    comment_id = db.StringProperty(required=True)
    post_id = db.StringProperty(required=True)
    timestamp = db.StringProperty(required=True)
    points = db.IntegerProperty(required=True, default=0)
    
    
class Organization(db.Model):
    name = db.StringProperty(required=True)
    added_by = db.StringProperty(required=True)
    email = db.StringProperty(required=False)
    address = db.StringProperty(required=False)
    city = db.StringProperty(required=False)
    state = db.StringProperty(required=False)
    country = db.StringProperty(required=False)
    notes = db.TextProperty(required=False)
    lat = db.StringProperty(required=False)
    lng = db.StringProperty(required=False)
    
class FlagPost(db.Model):
    post_id = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    tags = db.StringProperty(required=True)
    entry = db.TextProperty(required=True)
    tags_list = db.StringListProperty(required=True)
    timestamp = db.StringProperty(required=True)
    points = db.IntegerProperty(required=True)
    added_by = db.IntegerProperty(required=True)
    
class FlagComment(db.Model):
    comment = db.TextProperty(required=True)
    email = db.StringProperty(required=True)
    comment_id = db.StringProperty(required=True)
    post_id = db.StringProperty(required=True)
    timestamp = db.StringProperty(required=True)
    points = db.IntegerProperty(required=True, default=0)
    
class PlusMinusConstraints(db.Model):
    post_id = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    points = db.IntegerProperty(required=True)
    
class CommentPlusMinusConstraints(db.Model):
    comment_id = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    points = db.IntegerProperty(required=True)
    
class Invites(db.Model):
    invite_hash = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    
class Feedback(db.Model):
    feedback = db.TextProperty(required=True)
    