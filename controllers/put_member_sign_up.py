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
from controllers.show_error_html import show_error_html
from controllers.datastore_results import datastore_results
from controllers.get_hash import get_hash
from controllers.check_invite_email_and_hash import check_invite_email_and_hash
from controllers.delete_invite import delete_invite



def put_member_sign_up(self):
    logging.debug("sign_in_user")
    email = self.request.get("email")
    password = self.request.get("password")
    password2 = self.request.get("password2")
    invite_hash = self.request.get("invite_hash")
    
    filters = {
        "email": email,
    }
    
    results, results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
    
    if results_exist:
        show_error_html(self, "email already exists error")
        return False
        
    
    if password == password2:
        category = "Volunteer"
        try:
            
            if check_invite_email_and_hash(email = email, invite_hash = invite_hash):
                hashed_password = get_hash(password)
                m = model.Member(email = email, password = hashed_password, category = category, skills_list = [""])
                m.put()
                delete_invite(invite_hash = invite_hash, invite_email = email)
            else:
                show_error_html(self, "Not the correct email for this invite.")
                logging.debug("Incorrect email for invite")
                return False
        except:
            logging.debug("datastore error")
            show_error_html(self, "database error")
            
            
        try:
            session = get_current_session()
            session['email'] = email
            session['member'] = True
        except:
            logging.debug("gaesessions error")
            show_error_html(self, "session error")
        
        
        return True
    else:
        show_error_html(self, "The passwords are not the same, press back and try again.")
        