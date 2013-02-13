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
from geopy import geocoders  
import random
def put_organization_info(self):
    logging.debug("put_organization_info")
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
            name = self.request.get("name")
            organization = self.request.get("organization")
            email = self.request.get("email")
            street_address = self.request.get("street_address")
            city = self.request.get("city")
            state = self.request.get("state")
            country = self.request.get("country")
            notes = self.request.get("notes")
            address = street_address + " " + city + " " + state + " " + country
            print address

            
            if not state:
                address = street_address + " " + city + " " + country
            
            g = geocoders.OpenMapQuest()
            place, (lat, lng) = g.geocode(address)  
                
            filters = {
                "name": name,
            }
            results, results_exist = datastore_results("Organization", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
            
            key = None
            for result in results:
                key = result.key()
                
            if key is not None:                    
                o = model.Organization.get(key)
                o.email = email
                o.address = address
                o.city = city
                o.state = state
                o.country = country
                o.notes = notes
                lat_string = str(lat)
                lng_string = str(lng)
                o.lat = lat_string
                o.lng = lng_string
                o.put()
                
    else:
        self.redirect("/")