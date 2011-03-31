#!/usr/bin/env python

import os
from models import Book
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class BookHandler(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/book.html')

		book = get_book(self)

		if users.is_current_user_admin():
			admin = True
		else:
			admin = False

		template_values = {
			'book': book,
			'admin': admin,
		}

		self.response.out.write(template.render(path, template_values))


class BookEditor(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/edit.html')

		book = get_book(self)

		template_values = {
			'book': book,
		}

		self.response.out.write(template.render(path, template_values))

	def post(self):
		book = get_book(self)

		book.key = book.key
		book.cover = book.cover
		book.rating = self.request.get('rating').strip()
		book.title = self.request.get('title').strip()

		book.summary = self.request.get('summary').strip()
		book.first = self.request.get('first').strip()
		book.second = self.request.get('second').strip()
		book.third = self.request.get('third').strip()

		book.notes = self.request.get('notes')

		book.amazon_link = db.Link(self.request.get('amazon')).strip()

		book.url = self.request.get('title').replace(' ', '').lower()

		book.put()

		self.redirect('/%s' % book.url)


def get_book(self):
	book_url = (self.request.path).rpartition('/')
	book = db.GqlQuery("SELECT * FROM Book WHERE url = :1", book_url[2]).get()

	return book


def main():
	application = webapp.WSGIApplication([('/edit/.*', BookEditor),
										  ('/.*', BookHandler)],
										  debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()

