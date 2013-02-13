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

from controllers.check_login_2 import check_login_2


def delete_comment(comment_id):
    logging.debug("delete_comment")
    if check_login_2():
        session = get_current_session()
        email = session['email']
        filters = {
            "email": email,
            "comment_id": comment_id,
        }
        results, results_exist = datastore_results("Comment", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
        if not results_exist:
            return False
        
        for result in results:
            key = result.key()
            db.delete(key)
            return True
    else:
        return False