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

def datastore_results(kind, filters, inequality_filters, order, fetch_total, offset, mem_key):
    logging.debug("datastore_results")
    # a function to query the datastore and return results
    #### Start with a memcache check
    #### If no memcache, run query, then set memcache
    logging.debug("PageFunctions.datastore_results")  
    data = None
    if mem_key is not None:            
        logging.debug("mem_key is not None")
        data = memcache.get(mem_key)
        #To turn off memcache use for testing purposes, uncomment the next line
        #data = None
    if data is not None:
        logging.debug("data is not None")
        results_exist = True
        return data, results_exist
        
    else:        
        logging.debug("mem_key is Empty, performing datastore search")
        filter_key_list = []
        filter_value_list = []
        inequality_filter_key_list = []
        inequality_filter_value_list = []

        q = None
        # conditional search on the 'kind' parameter.
        # check the 'kind' parameter to find out what entity we will search and start the query
        try:
            if kind == "Member":
                q = model.Member.all()
            if kind == "Post":
                q = model.Post.all()
            if kind == "Tag":
                q = model.Tag.all()
            if kind == "Comment":
                q = model.Comment.all()
            if kind == "Organization":
                q = model.Organization.all()
                
        except:
            #self.redirect('/?' + urllib.urlencode({'error': 1}))
            pass
        # if the filters parameter is not None, add the filters into lists to be run later.
        if filters:
            for item in filters:
                filter_key_list.append(item)
                filter_value_list.append(filters[item])
        
        # if the lists are populated, run a filter for each member of the lists
        # filter_key_list has the search parameter
        # filter_value_list has the search value
        if filter_key_list:
            i = 0
            for key in filter_key_list:
                try:
                    q.filter(filter_key_list[i], filter_value_list[i])
                except:
                    #self.redirect('/?' + urllib.urlencode({'error': 1}))
                    pass
                i += 1

        if inequality_filters:
            for item in inequality_filters:
                inequality_filter_key_list.append(item)
                inequality_filter_value_list.append(inequality_filters[item])
        
        # if the lists are populated, run a filter for each member of the lists
        # filter_key_list has the search parameter
        # filter_value_list has the search value
        if inequality_filter_key_list:
            i = 0
            for key in inequality_filter_key_list:
                try:
                    q.filter(inequality_filter_key_list[i] + " !=" + inequality_filter_value_list[i])
                except:
                    #self.redirect('/?' + urllib.urlencode({'error': 1}))
                    logging.debug("error in inequality_filter")
                    pass
                i += 1

            # if the order parameter is not None, add an order to the query
        if order:
            try:
                q.order(order)
            except:
                #self.redirect('/?' + urllib.urlencode({'error': 1}))
                pass
            
        # get the results with fetch
        # use fetch_total and offset parameters to set up your function
        # try:
        results = q.fetch(fetch_total, offset = offset)
        #results = results[2:]
        if mem_key is not None:
            
            num = memcache.set(mem_key, results, 3600)  
            logging.debug("setting new memcache")
        results_exist = False
        if results:
            results_exist = True
        return results, results_exist