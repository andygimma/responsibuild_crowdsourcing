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
    body_first =  """
    You've been invited!
    Our Responsibuild hub will showcase best practices ranging from rebuilding your basement with better materials to what kind of mold-resistant paint to buy when you go to your local store.    We are a project
    """
    body = "To accept invite, go to 3rorg-test.appspot.com/?accept_invite=%s" % invite_hash
    if email == confirm_email:        
        message = mail.EmailMessage(sender=sender,
        subject="\nYou've been invited to a new Sustainable Rebuilding project!")
        
        message.to = "%s <%s>" % (email, email)
        message.body = body_first + body
            
        message.send()
        return True
        
    else:
        return False