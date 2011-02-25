#!/usr/bin/env python

import os
import cgi
from models import Book
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class MainHandler(webapp.RequestHandler):
    def get(self):
			path = os.path.join(os.path.dirname(__file__), 'templates/index.html')

			books = db.GqlQuery("SELECT * FROM Book ORDER BY date")

			template_values = {
				'books': books,
			}

			self.response.out.write(template.render(path, template_values))


#class BookHandler(webapp.RequestHandler):
#	def get(self):
#		file_name = self.request.path.replace('/', '') + '.html'
#		path = os.path.join(os.path.dirname(__file__), file_name)
#		template_values = {}
#		self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

                                      #    ('/.*', BookHandler)],

if __name__ == '__main__':
    main()
