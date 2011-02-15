#!/usr/bin/env python

import os
import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Book(db.Model):
	# Meta-data
	date = db.DateProperty(auto_now_add=True)
	rating = db.StringProperty()
	title = db.StringProperty()

	# Content
	summary = db.StringProperty(multiline=True)
	takeaways = db.StringProperty(multiline=True)
	notes = db.StringProperty(multiline=True)


class MainHandler(webapp.RequestHandler):
    def get(self):
			path = os.path.join(os.path.dirname(__file__), 'index.html')

			books = db.GqlQuery("SELECT * FROM Book ORDER BY date")

			template_values = {}
			self.response.out.write(template.render(path, template_values))


class BookHandler(webapp.RequestHandler):
	def get(self):
		file_name = self.request.path.replace('/', '') + '.html'
		path = os.path.join(os.path.dirname(__file__), file_name)
		template_values = {}
		self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/.*', BookHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
