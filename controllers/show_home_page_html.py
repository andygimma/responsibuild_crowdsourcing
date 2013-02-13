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
from controllers.datastore_results import datastore_results
from controllers.check_login import check_login


def show_home_page_html(self):
    logging.debug("show_home_page_html")
    #try:
    if check_login(self):
        path = os.path.join(os.path.dirname(__file__))
        path_length = path.__len__()
        final_path = path[0:path_length-11] + 'views/htmls/member_home_html.html'
        
        logging.debug("path = " + path)
        logging.debug("final_path = " + final_path)
        
        session = get_current_session()
        email = session['email']
        logged_in = check_login(self)
        filters = {
            "email": email,
        }
        
        member_results, member_results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1000, offset = 0, mem_key = None)
        finished_organizations_list = []
        unfinished_organizations_list = []
        original_organizations_list = []
        for result in member_results:
            original_organizations_list = result.orgs_list
        
        for name in original_organizations_list:
            filters = {
                "name": name,
            }
            
            results, results_exist = datastore_results("Organization", filters = filters, inequality_filters = None, order = None, fetch_total = 1000, offset = 0, mem_key = None)
            for result in results:
                city = result.city
                if city:
                    finished_organizations_list.append(name)
                else:
                    unfinished_organizations_list.append(name)
                
            
        error_message = "MEMBER HOME PAGE... CONTROL NOT FINISHED"
        data = {
            "error_message": error_message,
            "title_kind": "About Me:",
            "member_results": member_results,
            "logged_in": logged_in,
            "finished_organizations_list": finished_organizations_list,
            "unfinished_organizations_list": unfinished_organizations_list,
        }
        
        
        
        
        self.response.out.write(template.render(final_path, data))         
        #except:
            #logging.debug("exception")
        #show_error_html(self, "template error")
    else:
        self.redirect("/")