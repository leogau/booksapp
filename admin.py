#!/usr/bin/env python

import os
import cgi
import string

from models import Book

from google.appengine.api import users
from google.appengine.api import images

from google.appengine.ext import db
from google.appengine.ext import webapp

from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class AdminHandler(webapp.RequestHandler):
    def get(self):

        if users.is_current_user_admin():
            url = users.create_logout_url('/admin')
            url_linktext = 'Logout'
            path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
            template_values = {
                'url': url,
                'url_linktext': url_linktext,
            }   
            self.response.out.write(template.render(path, template_values))

            #enter_books(self)

        else:
            self.redirect(users.create_login_url(self.request.uri))


class BookHandler(webapp.RequestHandler):
    def post(self):
        book = Book()

        book.rating = self.request.get('rating')
        book.title = self.request.get('title')

        book.summary = self.request.get('summary')
        book.first = self.request.get('first')
        book.second = self.request.get('second')
        book.third = self.request.get('third')

        book.notes = self.request.get('notes')
        
        book.amazon_link = db.Link(self.request.get('amazon'))
        book.url = self.request.get('title').replace(' ', '').lower()

        book.cover = self.request.get('img')

        book.put()

        self.redirect('/')


class ImageHandler(webapp.RequestHandler):
    def get(self):
        book = db.get(self.request.get("img_id"))

        if book.cover:
            img = images.Image(book.cover)
            img.resize(width=350, height=550)
	    img.im_feeling_lucky()
            cover = img.execute_transforms(output_encoding=images.JPEG)

            self.response.headers['Content-Type'] = "image/jpeg"
            self.response.out.write(cover)
        else:
            self.response.out.write("No image")


def main():
    application = webapp.WSGIApplication(
                                          [('/admin', AdminHandler),
                                           ('/admin/new', BookHandler),
                                           ('/images', ImageHandler)],
                                          debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

