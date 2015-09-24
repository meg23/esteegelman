#!/usr/bin/env python

import webapp2
import logging
import json
import os

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext.webapp import template

log = logging.getLogger('webapp')

class SiteData(db.Model):

    element_name = db.StringProperty()
    element_title = db.StringProperty()
    element_content = db.StringProperty(multiline=True)
    element_order = db.IntegerProperty()
    testimonial_name = db.StringProperty()
    testimonial_designation = db.StringProperty()
    testimonial_image_url = db.StringProperty()

class Content(object):

    def get_single_content(self, element_name):
        element = db.GqlQuery("select * from SiteData where element_name = :1", element_name).get()
        return element

    def get_batch_content(self, element_name):
        elements = db.GqlQuery("select * from SiteData where element_name = :1 order by element_order", element_name)
        return elements

class Index(webapp2.RequestHandler):
    
    def get(self):
       
        content = Content() 

        template_values = {
            'headline': content.get_single_content('headline'),
            'headline_button': content.get_single_content('headline_button'),
            'bullet_blue': content.get_single_content('bullet_one'),
            'bullet_green': content.get_single_content('bullet_two'),
            'bullet_orange': content.get_single_content('bullet_three'),
            'testimonials': content.get_batch_content('testimonial_front')
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Contact(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'header_title': "Contact Estee",
            'header_body': "Her goal is to simplify difficult technologies in order to make them accessible to everyone. Discover how easy and enjoyable it can be to connect online, with a little help from Estee."
        }
        path = os.path.join(os.path.dirname(__file__), 'contact.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        contact_name = self.request.get('name')
        contact_email = self.request.get('email')
        contact_subject = self.request.get('subject')
        contact_message = self.request.get('message') + "\n Signed %s, %s" % (contact_name, contact_email)

        message = mail.EmailMessage(sender="estee@esteegelman.appspotmail.com",
                            subject=contact_subject)
        message.to = "estee@esteegelman.com"
        message.body = contact_message
        message.send()

        template_values = {
            'header_title': "Thanks for reaching out %s!" % (contact_name.capitalize()),
            'header_body': "She will get back to you soon, I promise."
        }
        path = os.path.join(os.path.dirname(__file__), 'contact.html')
        self.response.out.write(template.render(path, template_values))

class Meet(webapp2.RequestHandler):

    def get(self):

        content = Content() 

        template_values = {
            'bio': content.get_single_content('bio')
        }

        path = os.path.join(os.path.dirname(__file__), 'meet.html')
        self.response.out.write(template.render(path, template_values ))

class Testimonials(webapp2.RequestHandler):

    def get(self):

        content = Content()

        template_values = {
            'testimonials': content.get_batch_content('testimonial')
        }
        path = os.path.join(os.path.dirname(__file__), 'testimonials.html')
        self.response.out.write(template.render(path, template_values ))

app = webapp2.WSGIApplication([('/', Index ), ( '/contact', Contact), ('/meet', Meet), ('/testimonials', Testimonials) ], debug=True)


