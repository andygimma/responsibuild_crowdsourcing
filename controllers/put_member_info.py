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
from controllers.put_organization import put_organization





def put_member_info(self):
    logging.debug("sign_in_user")
    
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
        
        
    if continue_boolean:
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        twitter = self.request.get("twitter")
        organizations = self.request.get("organizations")
        anything_else = self.request.get("anything_else")
        city = self.request.get("city")
        state = self.request.get("state")
        country = self.request.get("country")
        
        if state:
            location = city + " " +  state + " " + country
        else:
            location = city + " " + country
        
        filters = {
            "email": email,
        }
        
        results, results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
        organizations_list = []
        final_list = []
        organizations = organizations.lower()
        organizations_list = organizations.split(",")
        for item in organizations_list:
            final_item = item.strip()
            final_list.append(final_item)
            put_organization(final_item)
        
        
        if results_exist:
            key = None
            for result in results:
                key = result.key()
                
            if key is not None:
                try:
                    
                    m = model.Member.get(key)
                    m.first_name = first_name
                    m.last_name = last_name
                    m.twitter = twitter
                    m.orgs = organizations
                    m.orgs_list = final_list
                    m.anything_else = anything_else
                    m.location = location
                    m.put()  
                
                    return True
                except:
                    return False
                    
            else:
                return False
                
        else:
            return False