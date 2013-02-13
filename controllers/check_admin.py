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
import settings


def check_admin():
    logging.debug("check_login")
    logged_in = False
    session = get_current_session()
    
    try:
        if session['member'] == True:
            email = session['email']
            logging.debug("session member is True")
            logged_in = True
        else:
            logging.debug("session member is False")
            logged_in = False
    except:
        logging.debug("session member exception, gaesession does not exist, return False")
        logged_in = False

    if logged_in:
        logged_in = False
        for admin in settings.ADMINS:
            if admin == email:
                logged_in = True
                
    return logged_in