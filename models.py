from google.appengine.ext import db

class Book(db.Model):
	# Meta-data
	date = db.DateProperty(auto_now_add=True)
	rating = db.StringProperty()
	title = db.StringProperty()
	amazon_link = db.LinkProperty()
	url = db.StringProperty()
	cover = db.BlobProperty()
	
	# Content
	summary = db.StringProperty(multiline=True)
	first = db.StringProperty(multiline=True)
	second = db.StringProperty(multiline=True)
	third = db.StringProperty(multiline=True)
	notes = db.TextProperty()


