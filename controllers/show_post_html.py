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
from controllers.datastore_results import datastore_results


def show_post_html(self, post_id):
    logging.debug("show_post_html")
    #try:
    path = os.path.join(os.path.dirname(__file__))
    path_length = path.__len__()
    final_path = path[0:path_length-11] + 'views/htmls/show_post.html'
    
    logging.debug("path = " + path)
    logging.debug("final_path = " + final_path)
                
    filters = {
        "post_id": post_id,
    }
    
    results, results_exist = datastore_results("Post", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
    
    
    filters = {
        "post_id": post_id,
    }
    
    comment_results, comment_results_exist = datastore_results("Comment", filters = filters, inequality_filters = None, order = None, fetch_total = 1000, offset = 0, mem_key = None)
    login_check = check_login(self)

    data = {
        "post_results": results,
        "logged_in": login_check,
        "comment_results": comment_results,
        "title_kind": "About Post",
     }
    
    
    self.response.out.write(template.render(final_path, data))         
    #except:
        #logging.debug("exception")
        #show_error_html(self, "template error")