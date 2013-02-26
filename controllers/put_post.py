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
from controllers.get_date_time import get_date_time
from controllers.get_hash import get_hash
from controllers.check_post_duplicates import check_post_duplicates



import random




def put_post(self):
    logging.debug("put_post")
    if check_login(self):
        
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
            title = self.request.get("title")
            tags = self.request.get("tags")
            entry = self.request.get("entry")
            old_hash = self.request.get("old_hash")

            
            tags_list = []
            final_list = []
            tags = tags.lower()
            tags_list = tags.split(",")
        
            for item in tags_list:
                final_item = item.strip()
                put_tag(self, final_item)
                
                final_list.append(final_item)
            new_hash = get_hash()
            timestamp = get_date_time()
            key = check_post_duplicates(old_hash)
            if key:
                p = model.Post.get(key)
                p.title = title
                p.tags = tags
                p.entry = entry
                p.tags_list = final_list
                p.timestamp = timestamp
                p.put()
                return old_hash
                
            p = model.Post(post_id = new_hash, email = email, title = title, tags = tags, entry = entry, tags_list = final_list, timestamp = timestamp, points=0)
            p.put()
            
            filters = {
                "email": email,
            }
            results, results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
            if results_exist:
                for result in results:
                    key = result.key()
                    points = result.rep_points
                    
                    member = model.Member.get(key)
                    member.rep_points = points + 10
                    member.put()
            
            return new_hash        
    else:
        self.redirect("/")