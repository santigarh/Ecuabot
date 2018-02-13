import os
class Config(object):
	SECRET_KEY = 'my_secret_token'
	PAGE_ACCESS_TOKEN = 'EAALNVNIGZAKEBAIwUgeUYkDd1PE5686XBbyerm1mVG6SLkvKRKheVJPe6FF4HfFMBKGR5z6SDIAlSvZAXyWxeR2lSwn1QevvB8gFnukDzrVZBiQEeqZC7WuG4X4m6O4K4uXkaWhl56nDUFQrsOUDYFVzPnwyrWwQ0npTabq7PgZDZD'
	USER_GEONAMES = os.environ.get('USER_GEONAMES') or 'santigar'
	PLACES_KEY = 'AIzaSyDzULJe8HoQ7LkIPtIfT_LNaE47bduqdA0' 
	
class DevelopmentConfig(Config):
	DEBUG = True