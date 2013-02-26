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
from controllers.check_admin import check_admin
from controllers.get_hash import get_hash
from controllers.put_invite_hash import put_invite_hash

from google.appengine.api import mail
from google.appengine.api import users



def send_invite(self):
    logging.debug("send_invite")
    email = self.request.get("email")
    confirm_email = self.request.get("confirm_email")
    invite_hash = get_hash()
    put_invite_hash(email = email, invite_hash = invite_hash)
    sender = "3Rorg Crowdsourcing Invite <%s>" % "responsibuildorg@gmail.com"
    logging.debug("sender" + sender)
    
    body_first = "Hello " + email
    body_edited = """    
    
    
    You're receiving this invite from the team behind Responsibuild, a hackathon award-winning project focused on creating a hub for survivors of disasters to rebuild their homes, communities, and lives.
    
    
    
    We're building a site of best practices and best materials for rebuilding in the wake of a natural disaster, such as a hurricane, flood, tornado, etc.  Our project was created in response to Hurricane Sandy and the wide scoping impact it had on the New York City community.
    
    
    
    Thank you for joining and for contributing your expert take and advice on issues such as mold remediation, most sustainable building materials (that are also economically affordable), and on how to best rebuild a home or community to weather future inevitable disasters and storms.
    
    
    
    With gratitude,
    
    
    
    Responsibuild (Andy, Ana, and Erica)
    
    """
    body_last = "To accept invite, go to 3rorg-test.appspot.com/?accept_invite=%s" % invite_hash
    finished_body = body_first + body_edited + body_last
    if email == confirm_email:        
        message = mail.EmailMessage(sender=sender,
        subject="\n!")
        
        message.to = "%s <%s>" % (email, email)
        message.body = finished_body
            
        message.send()
        return True
        
    else:
        return False