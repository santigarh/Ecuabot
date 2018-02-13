from flask import Flask
from flask import request

import json
from config import DevelopmentConfig

from handler import recived_message
from handler import recived_postback

from api import call_set_started_button
from api import greeting_text



app= Flask(__name__)
app.config.from_object( DevelopmentConfig )
#{u'entry': [{u'messaging': [{u'timestamp': 1510271448496L, u'message': {u'text': u'Hola', u'mid': u'mid.$cAAdYzIEnjf9l1Ha9sFfozFoWOD51', u'seq': 464536}, u'recipient': {u'id': u'2067961996563280'}, u'sender': {u'id': u'1261908763914783'}}], u'id': u'2067961996563280', u'time': 1510271550397L}], u'object': u'page'}
@app.route('/webhook', methods = ['GET' , 'POST'])
def webhook():
	if request.method == 'GET':
		verify_token= request.args.get('hub.verify_token', '')
		if verify_token == app.config['SECRET_KEY']:
			return request.args.get('hub.challenge', '')
		return 'Error al validar el secreto'
	
	elif request.method == 'POST':
		payload = request.get_data()
		data = json.loads(payload)
		
		
		for page_entry in data['entry']:
			for message_event in page_entry['messaging']:
				if 'message' in message_event:
					recived_message(message_event, app.config['PAGE_ACCESS_TOKEN'], app.config['USER_GEONAMES'] )
					
				if 'postback' in message_event:
					recived_postback( message_event, app.config['PAGE_ACCESS_TOKEN'])
					print("Hay un evento de postback")
				
		return "ok"
	
@app.route('/', methods = ['GET'])
def index():
	return 'Hola Amiguitos'

if __name__ == '__main__':
	call_set_started_button(app.config['PAGE_ACCESS_TOKEN'])
	greeting_text(app.config['PAGE_ACCESS_TOKEN'])
	app.run(port = 8000 )