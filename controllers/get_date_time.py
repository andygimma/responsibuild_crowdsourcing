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
from controllers.put_tag import put_tag
import random
from datetime import datetime, timedelta





def get_date_time():
    logging.debug("get_date_time")
    dt = datetime.now()
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    millisecond = dt.microsecond
    dtime = datetime(year, month, day, hour, minute, second, millisecond).isoformat()
    dtime2 = dtime.replace("-", "")
    dtime3 = dtime2.replace("T", "")
    dtime4 = dtime3.replace(":", "")
    dtime5 = dtime4.replace(".", "")
    final_time_string = dtime5[:-3]
    logging.debug("final_time_string = " + final_time_string)
    return final_time_string
    
    
    