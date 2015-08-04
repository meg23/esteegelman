#!/usr/bin/env python

import webapp2
import logging
import json
import os

from google.appengine.ext.webapp import template

log = logging.getLogger('webapp')

class Index(webapp2.RequestHandler):

    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, ""))

app = webapp2.WSGIApplication([('/', Index )], debug=True)


