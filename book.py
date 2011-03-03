#!/usr/bin/env python

import os
from models import Book
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class BookHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/book.html')

        book_url = (self.request.path).replace('/', '')
#        self.response.out.write(book_title)
        book = db.GqlQuery("SELECT * FROM Book WHERE url = :1", book_url).get()
#        book = Book.gql("WHERE title = 'Steve'").get()

        template_values = {
            'book': book,
        }

        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([('/.*', BookHandler)],
                                          debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

