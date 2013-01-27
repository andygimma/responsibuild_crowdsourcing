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
from controllers.show_error_html import show_error_html
import hashlib
import urlparse


def show_member_sign_up_form(self):
    logging.debug("show_admin_sign_up_form")
    #try:
    url =  self.request.url
    parsed = urlparse.urlparse(url)
    invite_hash = urlparse.parse_qs(parsed.query)['accept_invite']
    final_invite_hash = None
    for i in invite_hash:
        final_invite_hash = i
    
    path = os.path.join(os.path.dirname(__file__))
    path_length = path.__len__()
    final_path = path[0:path_length-11] + 'views/htmls/member_sign_up_form.html'

    logging.debug("path = " + path)
    logging.debug("final_path = " + final_path)
    
   
    data = {
        "invite_hash": invite_hash,
    }
    
    self.response.out.write(template.render(final_path, {'invite_hash': final_invite_hash}))         
    #except:
        #logging.debug("exception")
        #show_error_html(self, "template error")
        