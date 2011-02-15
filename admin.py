#!/usr/bin/env python

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Admin(webapp.RequestHandler):
	def get(self):


def main():
	application = webapp.WSGIApplication([('/', Admin)],
										  debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()

