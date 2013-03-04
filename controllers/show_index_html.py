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
from controllers.check_login import check_login
from controllers.show_error_html import show_error_html
from controllers.datastore_results import datastore_results
from controllers.get_hash import get_hash
from models import model




def show_index_html(self):
    logging.debug("show_index_html")
    session = get_current_session()
    staff_boolean = False
    try:
        staff_boolean = session['staff']
    
    except:
        staff_boolean = False
        
    if staff_boolean:
        try:
            path = os.path.join(os.path.dirname(__file__))
            path_length = path.__len__()
            final_path = path[0:path_length-11] + 'views/htmls/index_staff.html'
            
            logging.debug("path = " + path)
            logging.debug("final_path = " + final_path)
            
            logged_in = check_login(self)
                
                
            data = {
                "logged_in": logged_in,
            }
            
            
            self.response.out.write(template.render(final_path, data))         
        except:
            logging.debug("exception")
            show_error_html(self, "template error")
    else:
        #try:
        path = os.path.join(os.path.dirname(__file__))
        path_length = path.__len__()
        final_path = path[0:path_length-11] + 'views/htmls/index.html'
        
        logging.debug("path = " + path)
        logging.debug("final_path = " + final_path)
        
        logged_in = check_login(self)
            
        results, results_exist = datastore_results("Post", filters = None, inequality_filters = None, order = None, fetch_total = 1000, offset = 0, mem_key = None)
            
        data = {
            "logged_in": logged_in,
            "post_results": results,
            "title_kind": "Timeline",
        }
        
        
        member_filters = {
            "first_name": "Admin"
        }
        results, results_exist = datastore_results("Member", filters = member_filters, inequality_filters = None, order = None, fetch_total = 1000, offset = 0, mem_key = None)
        
        if not results_exist:
            password = get_hash("sandytech")
            m = model.Member(first_name = "Admin", password = password, category="Volunteer", orgs_list = [""], email = "responsibuildorg@gmail.com")
            m.put()
        
        self.response.out.write(template.render(final_path, data))         
        #except:
            #logging.debug("exception")
            #show_error_html(self, "template error")