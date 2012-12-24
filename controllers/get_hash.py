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

import random




def get_hash(string = None):
    logging.debug("get_hash")
    seed = "4b9bb860b4934a7fa17d1bedf31b78679ed3fe5f"
    random_number = random.random()
    random_string = str(random_number)
    time = get_date_time()
    
    h = ""
    if string:
        hash_string = time + seed + string
        h = hashlib.sha1(seed + string)
        #print 3
    else:
        h = hashlib.sha1(time + random_string)
    new_hash = h.hexdigest()

    return new_hash
        
        