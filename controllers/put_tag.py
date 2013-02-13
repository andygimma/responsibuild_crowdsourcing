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
import random




def put_tag(self, tag):
    logging.debug("put_tag")
    if check_login(self):
            
        
        continue_boolean = False
        email = ""
        #try:
        session = get_current_session()
        email = session['email']
        continue_boolean = True
        #except:
        #logging.debug("gaesessions exception, do not continue")
        #continue_boolean = False
        #show_error_html(self, "session error")
        
        tag = tag.lower()
        tag = tag.strip()
        if continue_boolean:
            ### check db, if not in db put tag
            filters = {
                "tag": tag,
            }
            
            results, results_exist = datastore_results("Tag", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
            if results_exist:
                logging.debug("tag already exists")
            else:
                t = model.Tag(tag = tag)
                t.put()
                
    else:
        self.redirect("/")