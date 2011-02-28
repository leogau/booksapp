#!/usr/bin/env python

import os
import cgi
from models import Book
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import images
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class AdminHandler(webapp.RequestHandler):
    def get(self):

        if users.is_current_user_admin():
            enter_books(self)

        else:
            self.redirect(users.create_login_url(self.request.uri))


class BookHandler(webapp.RequestHandler):
    def post(self):
        self.response.out.write("in Book")
        book = Book()

        book.rating = self.request.get('rating')
        book.title = self.request.get('title')

        book.summary = self.request.get('summary')
        book.first = self.request.get('first')
        book.second = self.request.get('second')
        book.third = self.request.get('third')

        book.notes = cgi.escape(self.request.get('notes'))
        book.amazon_link = self.request.get('amazon_link')
#        cover = self.request.get('img')
        book.cover = self.request.get('img')

        book.put()

        self.redirect('/')


class ImageHandler(webapp.RequestHandler):
    def get(self):
        book = db.get(self.request.get("img_id"))
        if book.cover:
            self.response.headers['Content-Type'] = "image/jpg"
            self.response.out.write(book.cover)
        else:
            self.response.out.write("No image")


def enter_books(self):
    url = users.create_logout_url('/admin')
    url_linktext = 'Logout'
    path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
    template_values = {
        'url': url,
        'url_linktext': url_linktext,
    }   
    self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication(
                                          [('/admin', AdminHandler),
                                           ('/admin/new', BookHandler),
										   ('/images', ImageHandler)],
                                          debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

