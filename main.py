#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



####
#
#
#
#  Hub Com
#  
#  Tier 1
#  Hubs upload their basic needs, resources, cars and volunteers
#  They can add their resources, and change them as needed
#  Same with needs
#  As cars go out, the Car object will let all hubs (but specifically the hub they are arriving at) what resources they have, and perhaps and arrival time
#  
#  Also, volunteers can be better reached and activated
#  
#  
#  Tier 2
#  Within hubs, we want to keep track of who is where, and how resources are being moved
#  Hopefully from this information, we can find out how to more effectively move resources, including good, services and volunteers who provide them
#  
#  
#  Tier 3
#  Allow for canvassers to upload info directly from their canvas sheets
#  Have a location, names of those living their, volunteer who added it, and a basic 1-5 scale on how important the need.
#  
#  Have a basic checklist for immediate needs
#
#  
#  
#  Tasks: 
#  Change gaesessions cookie in appengine_config.py
#  Create a list of hubs that only an admin can add, this way we don't have people signin in who we don't want to.
#  
#  
#  Needs:
#  
#  Someone to sanitize inputs
#  $ to pay for it
#  memcache
#  
#  
####
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from gaesessions import get_current_session
import logging
#import model
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
import geopy
#from controllers.register import register

from controllers.show_member_sign_up_form import show_member_sign_up_form
from controllers.show_index_html import show_index_html
from controllers.show_member_login_form import show_member_login_form
from controllers.put_member_sign_up import put_member_sign_up
from controllers.check_login import check_login
from controllers.logout import logout
from controllers.show_member_info_form import show_member_info_form
from controllers.put_member_info import put_member_info
from controllers.login_member import login_member
from controllers.show_error_html import show_error_html
from controllers.show_search_volunteers_by_skill_form import show_search_volunteers_by_skill_form
from controllers.search_volunteers_by_skill import search_volunteers_by_skill
from controllers.datastore_results import datastore_results
from controllers.show_add_post_form import show_add_post_form
from controllers.put_post import put_post
from controllers.show_post_html import show_post_html
from controllers.show_comment_form import show_comment_form
from controllers.put_comment import put_comment
from controllers.show_tags_html import show_tags_html
from controllers.show_single_tag_html import show_single_tag_html
from controllers.show_organizations_html import show_organizations_html
from controllers.show_contacts_html import show_contacts_html
from controllers.show_contact_html import show_contact_html
from controllers.show_organization_html import show_organization_html
from controllers.show_home_page_html import show_home_page_html
from controllers.show_contact_us_html import show_contact_us_html
from controllers.show_about_us_html import show_about_us_html
from controllers.show_add_organization_info_form import show_add_organization_info_form
from controllers.put_organization_info import put_organization_info
from controllers.show_maps_html import show_maps_html
from controllers.get_hash import get_hash





template.register_template_library('my_filters')




class MainHandler(webapp.RequestHandler):
    def get(self):
        logging.debug("get_geocode")
        
        session = get_current_session()
        member_login_param = self.request.get("member_login")
        member_sign_up_param = self.request.get("member_sign_up")
        logout_param = self.request.get("logout")
        member_info_param = self.request.get("member_info")
        add_post_param = self.request.get("add_post")
        post_param = self.request.get("post")
        comment_param = self.request.get("comment")
        show_tags_param = self.request.get("showtags")
        single_tag_param = self.request.get("singletag")
        show_organizations_param = self.request.get("show_organizations")
        show_contacts_param = self.request.get("show_contacts")
        organization_param = self.request.get("organization")
        show_contact_param = self.request.get("contact")
        home_page_param = self.request.get("home_page")
        contact_us_param = self.request.get("contact_us")
        about_us_param = self.request.get("about_us")
        add_info_param = self.request.get("add_info")
        show_maps_param = self.request.get("show_maps")
        
        
        
        
        if member_login_param:
            logging.debug("member_login_param")
            show_member_login_form(self)
            # Here we need the controller that calls the login form and displays the template
        elif member_sign_up_param:
            show_member_sign_up_form(self)
            logging.debug("admin_sign_up_param")
            # Here we need the controller that calls the sign up form and displays the template
        elif logout_param:
            logout(self)
            logging.debug("logout")
            # logout the user by clearing gaesessions with session.clear()
            
        elif member_info_param:
            show_member_info_form(self)
            logging.debug("show_member_info_form")
            
        elif add_post_param:
            show_add_post_form(self)
            
        elif post_param:
            show_post_html(self, post_param)
            
        elif comment_param:
            show_comment_form(self, comment_param)
            
        elif show_tags_param:
            show_tags_html(self)
            
        elif single_tag_param:
            show_single_tag_html(self, single_tag_param)
            
        elif show_organizations_param:
            show_organizations_html(self)
            
        elif show_contacts_param:
            show_contacts_html(self)
            
        elif organization_param:
            show_organization_html(self, organization_param)
            
        elif show_contact_param:
            show_contact_html(self, show_contact_param)
            
        elif home_page_param:
            show_home_page_html(self)
            
        elif contact_us_param:
            show_contact_us_html(self)
            
        elif about_us_param:
            show_about_us_html(self)
            
        elif add_info_param:
            show_add_organization_info_form(self, add_info_param)
            
        elif show_maps_param:
            show_maps_html(self)
        else:
            logging.debug("main page")
            show_index_html(self)
            # need controller that displays index.html template
        


class MemberSignUp(webapp.RequestHandler):
    def post(self):
        saved = put_member_sign_up(self)
        if saved:
            session = get_current_session()
            session['member'] = True
            self.redirect('/?' + urllib.urlencode({'member_info': True}))
        
class MemberLogin(webapp.RequestHandler):
    def post(self):
        login_check = login_member(self)
        email = self.request.get("email")
        password = self.request.get("password")
        hashed_password = get_hash(password)
        filters = {
            "email": email,
            "password": hashed_password,
        }
        session = get_current_session()
        session.clear()
        
        results, results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1000, offset = 0, mem_key = None)
        if results_exist:
            session = get_current_session()
            session['member'] = True
            session['email'] = email
            
            if login_check:
            ### check for first name, if first name, go to main page
                session = get_current_session()
                session['member'] = True
                
                email = session['email']
                filters = {
                    "email": email,
                }
                
                results, results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
                first_name = None
                if results_exist:
                    for result in results:
                        first_name = result.first_name
                        
                if first_name is None:
                    self.redirect('/?' + urllib.urlencode({'member_info': True}))
                else:
                    self.redirect('/?' + urllib.urlencode({'home_page': True}))
                
                
        else:
            self.redirect('/?' + urllib.urlencode({'member_login': True}))
            
            #show_error_html(self, "email and password combination not found, press back to try again")

                
        
        
class MemberInfo(webapp.RequestHandler):
    def post(self):
        member_info_boolean = put_member_info(self)
        if member_info_boolean is True:
            self.redirect('/?' + urllib.urlencode({'home_page': True}))
        else:
            pass
            #show_error_html("database_error")
            

class SearchVolunteersBySkill(webapp.RequestHandler):
    def post(self):
        search_volunteers_by_skill(self)
        
class AddPost(webapp.RequestHandler):
    def post(self):
        post_id = put_post(self)
        self.redirect('/?' + urllib.urlencode({'post': post_id}))
        
            
            
class Comment(webapp.RequestHandler):
    def post(self):
        post_id = put_comment(self)
        self.redirect('/?' + urllib.urlencode({'post': post_id}))
        
class OrganizationInfo(webapp.RequestHandler):
    def post(self):
        put_organization_info(self)
        self.redirect('/?' + urllib.urlencode({'home_page': "True"}))
        
    
def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/member_sign_up', MemberSignUp),
        ('/member_login', MemberLogin),
        ('/member_info', MemberInfo),
        ('/search_volunteers_by_skill', SearchVolunteersBySkill),
        ('/add_post', AddPost),
        ('/comment', Comment),
        ('/organization_info', OrganizationInfo),
        
        ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
