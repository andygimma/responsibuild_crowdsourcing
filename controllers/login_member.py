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
from controllers.show_error_html import show_error_html
from controllers.get_hash import get_hash



def login_member(self):
    logging.debug("login_member")
    
    email = self.request.get("email")
    password = self.request.get("password")
    
    
    logging.debug("email = " + email)
    logging.debug("password = " + password)
    
    hashed_password = get_hash(password)
    logging.debug("hashed_password")
    #print hashed_password
    filters = {
        "email": email,
        "password": hashed_password,
    }
        
    results, results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
    category = ""
    for result in results:
        category = result.category
        
    try:
        session = get_current_session()
        session['member'] = True
        session['email'] = email
        if category == "Staff":
            session['staff'] = True
    except:
        logging.debug("gaesessions exception")
        show_error_html(self, "session error")
    
    if results_exist:
        return True
    else:
        return False