from google.appengine.ext import webapp
import model
from google.appengine.api import memcache
import logging
from controllers.datastore_results import datastore_results
from gaesessions import get_current_session
register = webapp.template.create_template_register()

#@register.simple_tag
@register.filter(name="email_to_rep_points")
def email_to_rep_points(email):
    filters = {
        "email": email
    }
    results, results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1000, offset = 0, mem_key = None)
    rep_points = ""
    for result in results:
        rep_points = result.rep_points
    return rep_points
    
    
@register.filter(name="check_ownership")
def check_ownership(email):
    session = get_current_session()
    session_email = None
    try:
        session_email = session['email']
    except:
        return False
    if session_email == email:
        return True
    else:
        return False
#####
# to be used this way

#{% if result.email|check_ownership %}
#<a href>Delete</a><a href>Edit</a>
#{% endif %}

#
#####
        
        
        
@register.filter(name='email_to_name')
def email_to_name(request):
    filters = {
        "email": request
    }
    results, results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1000, offset = 0, mem_key = None)
    name = ""
    for result in results:
        name = result.first_name
    return name
    
@register.filter(name='prettify')
def prettify(request):
    timezone = memcache.get("timezone")
    
    #if not timezone:
        #q = model.TimezoneOffset.all()
        #email = "email"
        #q.filter = ("email =", email)
        #results = q.fetch(1)
        #for result in results:
            #timezone = result.offset
            #mem_key = "timezone"
            #if not memcache.set(mem_key, timezone, 2592000):
                #logging.debug("memcache not set")
            #else:                
                #logging.debug("timezone memcache set")
                
    #logging.debug("timezone" + str(timezone))                   
    timezone = "-5"
    #mem_key = "timezone"
    #if not memcache.set(mem_key, timezone, 2592000):
        #logging.debug("memcache not set")
    #else:
        #logging.debug("memcache set")
        
        
    month = request[4:6]
    day = request[6:8]
    hour = request[8:10]
    minute = request[10:12]
    month_int = int(month)
    day_int = int(day)
    hour_int = int(hour)
    minute_int = int(minute)
    timezone_int = int(timezone)
    hour_int = hour_int + timezone_int
    if timezone_int < 0:
        if hour_int < 0:
            hour_int = hour_int + 24
            day_int = day_int - 1
            if day_int < 1:
                month_int = month_int - 1
                if month_int == 1:
                    day_int = 31
                if month_int == 2:
                    day_int = 28
                if month_int == 3:
                    day_int = 31
                if month_int == 4:
                    day_int = 30
                if month_int == 5:
                    day_int = 31
                if month_int == 6:
                    day_int = 30
                if month_int == 7:
                    day_int = 31
                if month_int == 8:
                    day_int = 31
                if month_int == 9:
                    day_int = 30
                if month_int == 10:
                    day_int = 31
                if month_int == 11:
                    day_int = 30
                if month_int == 12:
                    day_int = 31
            
            
        if month_int < 1:
            month_int = 12

        if month_int == 1:
            month = "January"
        if month_int == 2:
            month = "February"
        if month_int == 3:
            month = "March"
        if month_int == 4:
            month = "April"
        if month_int == 5:
            month = "May"
        if month_int == 6:
            month = "June"
        if month_int == 7:
            month = "July"
        if month_int == 8:
            month = "August"
        if month_int == 9:
            month = "September"
        if month_int == 10:
            month = "October"
        if month_int == 11:
            month = "November"
        elif month_int == 12:
            month = "December"
            
        if hour_int > 12:
            hour_int = hour_int - 12
        if hour_int == 0:
            hour_int == 12
        string_month = str(month_int)
        string_day = str(day_int)
        string_hour = str(hour_int)
        string_minute = str(minute_int)
        if len(string_minute) == 1:
            string_minute = "0" + string_minute
        
        #return month + " " + day + ", " + hour + ":" + minute
        return month + " " + string_day + ", " + string_hour + ":" + string_minute
        
    elif timezone_int > 0:
        if hour_int > 24:
            hour_int = hour_int - 24
            day_int = day_int + 1
            
        if day_int > 28:
            if month_int == 2:
                month_int = 3
                day_int = 1
               
        if day_int > 30:
            if month_int == 4:
                month_int = 5
                day_int = 1
            elif month_int == 6:
                month_int = 7
                day_int = 1
            elif month_int == 9:
                month_int = 10
                day_int = 1
            elif month_int == 11:
                month_int = 12
                day_int = 1
                
        if day_int > 31:
            day_int = 1
            month_int = month_int + 1
    
        if month_int == 1:
            month = "January"
        if month_int == 2:
            month = "February"
        if month_int == 3:
            month = "March"
        if month_int == 4:
            month = "April"
        if month_int == 5:
            month = "May"
        if month_int == 6:
            month = "June"
        if month_int == 7:
            month = "July"
        if month_int == 8:
            month = "August"
        if month_int == 9:
            month = "September"
        if month_int == 10:
            month = "October"
        if month_int == 11:
            month = "November"
        elif month_int == 12:
            month = "December"
            
        if hour_int > 12:
            hour_int = hour_int - 12
        if hour_int == 0:
            hour_int == 12
            
        string_month = str(month_int)
        string_day = str(day_int)
        string_hour = str(hour_int)
        string_minute = str(minute_int)
        if len(string_minute) == 1:
            string_minute = "0" + string_minute
        #return month + " " + day + ", " + hour + ":" + minute
        return month + " " + string_day + ", " + string_hour + ":" + string_minute        