from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from gaesessions import get_current_session
import logging
import model
import urllib
from google.appengine.ext import db
import random
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from os import environ
from google.appengine.api import memcache
from google.appengine.api import images
from google.appengine.api import oauth
import Cookie
import hashlib
from models import model
from controllers.datastore_results import datastore_results
from controllers.check_login import check_login
from controllers.show_error_html import show_error_html
from controllers.put_tag import put_tag
from controllers.get_date_time import get_date_time
from controllers.get_hash import get_hash
from geopy import geocoders  




import random




def put_invite_hash(invite_hash, email):
    logging.debug("put_invite_hash")
    i = model.Invites(email = email, invite_hash = invite_hash)
    i.put()
    
            
        