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

from wtforms import Form, BooleanField, TextField, validators, PasswordField, ValidationError

import wtforms
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
from controllers.put_post_plus_one import put_post_plus_one
from controllers.put_post_minus_one import put_post_minus_one
from controllers.put_post_flag import put_post_flag
from controllers.put_comment_flag import put_comment_flag
from controllers.put_comment_plus_one import put_comment_plus_one
from controllers.put_comment_minus_one import put_comment_minus_one
from controllers.show_send_invite_form import show_send_invite_form
from controllers.send_invite import send_invite
from controllers.put_feedback import put_feedback
from controllers.delete_post import delete_post
from controllers.delete_comment import delete_comment





import settings










#template.register_template_library('my_filters')
webapp.template.register_template_library('filters.my_filters')



class MainHandler(webapp.RequestHandler):
    def get(self):
        logging.debug("main")
        
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
        contact_us_param = self.request.get("feedback")
        about_us_param = self.request.get("about_us")
        add_info_param = self.request.get("add_info")
        show_maps_param = self.request.get("show_maps")
        send_invite_param = self.request.get("send_invite")
        accept_invite_param = self.request.get("accept_invite")
        edit_param = self.request.get("edit")
        delete_post_param = self.request.get("delete_post")
        delete_comment_param = self.request.get("delete_comment")
        
        
        
        
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
            
        elif send_invite_param:
            show_send_invite_form(self)
            
        elif edit_param:
            show_add_post_form(self, post_id = edit_param)
            
        elif accept_invite_param:
            show_member_sign_up_form(self)
            
        elif delete_post_param:
            delete_post(delete_post_param)
            self.redirect("/")
            
        elif delete_comment_param:
            delete_comment(delete_comment_param)
            self.redirect("/")
            
        else:
            logging.debug("main page")
            show_index_html(self)
            # need controller that displays index.html template
        


class MemberSignUp(webapp.RequestHandler):
    def post(self):
        form = SignInForm(self.request.POST)
        if not form.validate():
            path = os.path.join(os.path.dirname(__file__))
            path_length = path.__len__()
            final_path = path + '/views/htmls/member_sign_up_form.html'
            data = {
                'form': form,
            }
            self.response.out.write(template.render(final_path, data))     
        else:
            saved = put_member_sign_up(self)
            if saved:
                session = get_current_session()
                session['member'] = True
                self.redirect('/?' + urllib.urlencode({'member_info': True}))
        
class MemberLogin(webapp.RequestHandler):
    def post(self):
        form = SignInForm(self.request.POST)
        if not form.validate():
            path = os.path.join(os.path.dirname(__file__))
            path_length = path.__len__()
            final_path = path + '/views/htmls/member_login_form.html'
            #print final_path
            data = {
                'form': form,
            }
            self.response.out.write(template.render(final_path, data))         
        else:
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

class OrganizationForm(Form):
    notes = TextField('Describe your organizaiton', [
    validators.Length(min=20)
    ])
    email = TextField('Email', [
    validators.Length(min=6),
    validators.Email()
    ])
    
class InviteForm(Form):
    email = PasswordField('Email', [validators.Required(), validators.EqualTo('confirm_email', message='Email must match')])
    confirm_email  = PasswordField('Repeat Email')

    
class FeedbackForm(Form):
    feedback = TextField('Feedback', [
    validators.Length(min=20)
    ])

class PostForm(Form):
    tags = TextField('Subjects', [wtforms.validators.Length(min = 0, max = 100,
    message = "Subjects required")])
    tags = TextField('Tags', [validators.Required()])
    title = TextField('Title', [validators.Required()])
    entry = TextField('Entry', [
        validators.Length(min=20)
        ])
    def validate_length(self, form, field):
        if len(field.data) > 20:
            raise ValidationError('Entry too short')
    
    
class SignInForm(Form):
    email = TextField('Email', [
        validators.Length(min=6),
        validators.Email()
        ])
    password = TextField('Tags', [validators.Required()])
    
class SignUpForm(Form):
    email = TextField('Email', [
        validators.Length(min=6),
        validators.Email()
        ])
    password = TextField('Password', [validators.Required()])
    password2 = TextField('Password2', [validators.Required()])
    
class MemberInfoForm(Form):
    first_name = TextField('First Name', [validators.Required()])
    last_name = TextField('Last Name', [validators.Required()])
    #twitter = TextField('Password', [validators.Required()])
    # just check if it's a twitter handle
    city = TextField('City', [validators.Required()])
    #state = TextField('Password', [validators.Required()])
    country = TextField('Country', [validators.Required()])
    organizations = TextField('Organizations', [validators.Required()])
    #anything_else = TextField('Anything Else', [validators.Required()])
    
    
    
    
class MemberInfo(webapp.RequestHandler):
    def post(self):
        form = MemberInfoForm(self.request.POST)
        if not form.validate():
            path = os.path.join(os.path.dirname(__file__))
            path_length = path.__len__()
            final_path = path + '/views/htmls/member_info_form.html'
            #print final_path
            data = {
                'form': form,
            }
            self.response.out.write(template.render(final_path, data))         
        else:
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
        form = PostForm(self.request.POST)
        if not form.validate():
            path = os.path.join(os.path.dirname(__file__))
            path_length = path.__len__()
            final_path = path + '/views/htmls/add_post.html'
            logged_in = check_login(self)
            data = {
                "logged_in": logged_in,
                'form': form,
            }
            self.response.out.write(template.render(final_path, data))         
        else:         
            post_id = put_post(self)
            self.redirect('/?' + urllib.urlencode({'post': post_id}))
        
            
            
class Comment(webapp.RequestHandler):
    def post(self):
        is_valid, post_id = put_comment(self)
        self.redirect('/?' + urllib.urlencode({'post': post_id}))
        
class OrganizationInfo(webapp.RequestHandler):
    def post(self):
        form = OrganizationForm(self.request.POST)
        if not form.validate():
            path = os.path.join(os.path.dirname(__file__))
            path_length = path.__len__()
            final_path = path + '/views/htmls/show_add_organization_info_form.html'
            data = {
                'form': form,
            }
            self.response.out.write(template.render(final_path, data)) 
            return
        else:
            put_organization_info(self)
        self.redirect('/?' + urllib.urlencode({'home_page': "True"}))
        
class PlusOne(webapp.RequestHandler):
    def post(self):
        post_id = put_post_plus_one(self)
        self.redirect('/?' + urllib.urlencode({'post': post_id}))
        
class MinusOne(webapp.RequestHandler):
    def post(self):
        post_id = put_post_minus_one(self)
        self.redirect('/?' + urllib.urlencode({'post': post_id}))
        
class Flag(webapp.RequestHandler):
    def post(self):
        post_id = put_post_flag(self)
        self.redirect('/?')
        
class CommentFlag(webapp.RequestHandler):
    def post(self):
        post_id = put_comment_flag(self)
        self.redirect('/?' + urllib.urlencode({'post': post_id}))
        
class CommentPlusOne(webapp.RequestHandler):
    def post(self):
        post_id = put_comment_plus_one(self)
        self.redirect('/?' + urllib.urlencode({'post': post_id}))
        
class CommentMinusOne(webapp.RequestHandler):
    def post(self):
        post_id = put_comment_minus_one(self)
        self.redirect('/?' + urllib.urlencode({'post': post_id}))
        
class SendInvite(webapp.RequestHandler):
    def post(self):
        form = InviteForm(self.request.POST)
        if not form.validate():
            logged_in = check_login(self)
            path = os.path.join(os.path.dirname(__file__))
            path_length = path.__len__()
            final_path = path + '/views/htmls/show_send_invite_form.html'
            data = {
                'form': form,
                "logged_in": logged_in,
            }
            self.response.out.write(template.render(final_path, data)) 
            return
        else:
            if send_invite(self):
                self.redirect('/')
                return
            else:
                show_error_html(self, "Send invite didn't work, please contact us, or try again")
                
            
class SendFeedback(webapp.RequestHandler):
    def post(self):
        form = FeedbackForm(self.request.POST)
        if not form.validate():
            logged_in = check_login(self)
            path = os.path.join(os.path.dirname(__file__))
            path_length = path.__len__()
            final_path = path + '/views/htmls/contact_us_html.html'
            data = {
                "logged_in": logged_in,
                'form': form,
            }
            self.response.out.write(template.render(final_path, data))     
            return
        else:
            if put_feedback(self):
                self.redirect("/")
                logging.debug("feedback")
                return
            else:
                show_error_html(self, "Feedback didn't work, please email us and let us know what went wrong. Thanks!")
                logging.debug("feedback didn't work")
                return
    
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
        ('/plus_one', PlusOne),
        ('/minus_one', MinusOne),
        ('/flag', Flag),
        ('/comment_flag', CommentFlag),
        ('/comment_plus_one', CommentPlusOne),
        ('/comment_minus_one', CommentMinusOne),
        ('/send_invite', SendInvite),
        ('/send_feedback', SendFeedback),
        
        
        ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
