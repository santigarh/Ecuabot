import requests
import json


def call_geoname_API(lat, lng, username): #consumo Api del clima
	res = requests.get('http://api.geonames.org/findNearByWeatherJSON',
			params = {'lat': lat, 'lng': lng, 'username': username })
	
	if res.status_code == 200:
		res = json.loads(res.text)
		print res
		
		city = res['weatherObservation']['stationName']
		temperature = res['weatherObservation']['temperature']
		cloud = res['weatherObservation']['clouds']
		return {'city': city, 'temperature': temperature, 'cloud': cloud} #retorno un data_model

def call_geonamePlaces_API(lat, lng, username): #consumo Api del clima
	res = requests.get('http://api.geonames.org/findNearbyPlaceNameJSON',
			params = {'lat': lat, 'lng': lng, 'username': username })
			
	#{u'geonames': 
	#[{u'distance': u'0.62987', u'countryId': u'3658394', u'name': u'La Colina', u'countryCode': u'EC', 
	#u'geonameId': 11204068, u'toponymName': u'La Colina', u'fcode': u'PPL', u'fclName': u'city, village,...', 
	#u'fcodeName': u'populated place', u'countryName': u'Ecuador', u'lat': u'-0.31549', u'lng': u'-78.44047', 
	#u'adminName1': u'Pichincha', u'fcl': u'P', u'adminCode1': u'18', u'population': 0}]}
	if res.status_code == 200:
		res = json.loads(res.text)
				
		nombre =  res['geonames'][0]['name']
		administracion =  res['geonames'][0]['adminName1']
		lat = res['geonames'][0]['lat']
		lng = res['geonames'][0]['lng']
		
		return {'nombre': nombre, 'administracion': administracion, 'lat': lat, 'lng': lng }

def call_geonamePlaces_API_Dos(lat, lng, username): #consumo Api del clima
	res = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json',
			params = {'lat': lat, 'lng': lng, 'username': username })
			
	#{u'geonames': 
	#[{u'distance': u'0.62987', u'countryId': u'3658394', u'name': u'La Colina', u'countryCode': u'EC', 
	#u'geonameId': 11204068, u'toponymName': u'La Colina', u'fcode': u'PPL', u'fclName': u'city, village,...', 
	#u'fcodeName': u'populated place', u'countryName': u'Ecuador', u'lat': u'-0.31549', u'lng': u'-78.44047', 
	#u'adminName1': u'Pichincha', u'fcl': u'P', u'adminCode1': u'18', u'population': 0}]}
	if res.status_code == 200:
		res = json.loads(res.text)
				
		name =  res['geonames'][0]['name']
		administracion =  res['geonames'][0]['adminName1']
		lat = res['geonames'][0]['lat']
		lng = res['geonames'][0]['lng']
		
		return {'nombre': name, 'administracion': administracion, 'lat': lat, 'lng': lng }
				
def call_places_API(lat, lng, username, type):
	res = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json',
			params = {'location': repr(lat)+','+repr(lng), 'radius': '500', 'type': type, 'key':'AIzaSyDzULJe8HoQ7LkIPtIfT_LNaE47bduqdA0' })
	
	if res.status_code == 200:
		res = json.loads(res.text)
		print res
		#{u'status': u'ZERO_RESULTS', u'html_attributions': [], u'results': []}
		if res['status']== "ZERO_RESULTS":
			pass
		else:
			name = res['results'][0]['name']
			#photo = res['results']['photos'][0]['photo_reference']
			ubication = res['results'][0]['vicinity']
			
			return {'name': name, 'ubication': ubication }
			
		return res['status']

		
def call_send_API( data, token ):
	res = requests.post('https://graph.facebook.com/v2.6/me/messages',
					params = {'access_token': token },
					data = json.dumps(data),
					headers = { 'Content-type': 'application/json' }
					)
	if res.status_code == 200:
	 print "El mensaje fue enviado exitosamente!"
	 
def call_user_API(user_id, token):
	res = requests.get('https://graph.facebook.com/v2.6/' + user_id ,
					params = {'access_token': token } )

	data = json.loads(res.text)
	return data
	
def get_data():
	data = {
				'setting_type': 'call_to_actions',
				'thread_state': 'new_thread',
				'call_to_actions': [ {"payload": "COMENZAR_CHAT" } ] #
			}
	return data

def get_greeting_text():
	data = { "setting_type":"greeting",
  				"greeting":{ "text":"Bienvenido, EcuaBot - Tourism espera brindarte informacion muy util para ti" }
				}
	return data

def call_set_started_button(token):

				
		res = requests.post('https://graph.facebook.com/v2.6/me/thread_settings',
				params = {'access_token': token},
				data = json.dumps(get_data()),
				headers = {'Content-type': 'application/json'}
				)
		if res.status_code == 200:
			print(json.loads(res.text) )

def call_delete_started_button(token):
	res = requests.delete('https://graph.facebook.com/v2.6/me/thread_settings',
				params = {'access_token' : token},
				data = json.dumps( get_data() ),
				headers = { 'Content-type': 'application/json' } )

	if res.status_code == 200:
		print(json.loads(res.text) )

def greeting_text(token):
	res = requests.post('https://graph.facebook.com/v2.6/me/thread_settings',
				params = {'access_token' : token},
				data = json.dumps( get_greeting_text() ),
				headers = { 'Content-type': 'application/json' } )

	if res.status_code == 200:
		print(json.loads(res.text) )