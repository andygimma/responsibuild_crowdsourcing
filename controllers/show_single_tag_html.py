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
from controllers.delete_tag import delete_tag



def show_single_tag_html(self, tag):
    logging.debug("show_single_tag_html")
    path = os.path.join(os.path.dirname(__file__))
    path_length = path.__len__()
    final_path = path[0:path_length-11] + 'views/htmls/show_single_tag.html'
    
    logging.debug("path = " + path)
    logging.debug("final_path = " + final_path)
    logged_in = check_login(self)
    filters = {
        "tags_list": tag,
    }
    results, results_exist = datastore_results("Post", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
    
    no_results = False
    if results_exist == False:
        no_results = True
        delete_tag(tag)
    data = {
        "logged_in": logged_in,
        "tag_results": results,
        "title_kind": "All results with: " + tag,
        "no_results": no_results,
    }
    
    self.response.out.write(template.render(final_path, data))         
    #except:
        #logging.debug("exception")
        #show_error_html(self, "template error")