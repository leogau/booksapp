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

		book_url = (self.request.path).replace('/', '')
#self.response.out.write(book_title)
		book = db.GqlQuery("SELECT * FROM Book WHERE url = :1", book_url).get()
#book = Book.gql("WHERE title = 'Steve'").get()
#book = get_book(self)

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

		book_url = (self.request.path).lstrip('/edit')
		book = db.GqlQuery("SELECT * FROM Book WHERE url = :1", book_url).get()

#book = get_book(self)

		template_values = {
			'book': book,
		}

		self.response.out.write(template.render(path, template_values))

	def post(self):
		book = Book()
		
		book.rating = self.request.get('rating')
		book.title = self.request.get('title')

		book.summary = self.request.get('summary') if self.request.get('summary') != book.summary else book.summary
		book.first = self.request.get('first') if self.request.get('first') != book.first else book.first
		book.second = self.request.get('second') if self.request.get('second') != book.second else book.second
		book.third = self.request.get('third') if self.request.get('third') != book.third else book.third

		book.notes = self.request.get('notes') if self.request.get('notes') != book.notes else book.notes

		if book.amazon_link != db.Link(self.request.get('amazon')):
			book.amazon_link = db.Link(self.request.get('amazon'))

		book.url = (self.request.path).lstrip('/edit')

		book.put()

		self.redirect('/%s' % book.url)


def get_book(self):
	book_url = (self.request.path).lstrip('/edit')
	book = db.GqlQuery("SELECT * FROM Book WHERE url = :1", book_url).get()

	return book


def main():
	application = webapp.WSGIApplication([('/edit/.*', BookEditor),
										  ('/.*', BookHandler)],
										  debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()

