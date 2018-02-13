#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import UserModel
from models import MessageModel
#from models import TopicModel

import datetime
import threading
import time

from api import *
from data_bot import *

global_token = ''
global_username= ''
MAX_TIME = 10000

def recived_postback(event, token):
	sender_id = event['sender']['id']
	recipient_id = event['recipient']['id']
	time_postback = event['timestamp']
	payload = event['postback']['payload']

	global global_token
	global_token = token

	print payload

	handler_postback(sender_id, payload)

def handler_postback(user_id, payload):
	if payload == 'COMENZAR_CHAT':
		first_step(user_id)
	else: 
		user = UserModel.find(user_id = user_id)
		send_loop_messages(user, type_message= 'postback', context = payload )
	
		
def recived_message(event, token, username): #funcion que obtiene el mensaje del usuario
	sender_id = event['sender']['id']
	recipient_id = event['recipient']['id'] 
	time_message = event['timestamp']
	message =  event['message']
	print message
	global global_token, global_username #asigno variables globales
	global_token = token
	global_username = username
		
	handler_action(sender_id, message)
	
def handler_action(sender_id, message): #veo que accion necesito realizar
	user = UserModel.find( user_id = sender_id ) #valido si ya esta registrado en la base
	try_send_message(user, message)
	
def try_send_message(user, message):
	#listofComida = [ 'Comida', 'comer', 'almorzar', 'desayunar', 'merendar']
	flag =  validate_quick_replies(user, message) #valido si el mensaje es normal o un quick_replie o un attachment
	if flag is True:
		pass #flag = False
	else:
		message_lower = message['text'].lower()
		
		if 'ayuda' in message_lower:
			send_loop_messages(user, type_message='help', context = 'help')
		elif 'otra' in message_lower:
			send_loop_messages(user, type_message='other', context = 'welcome')
		elif 'keywords' in message_lower:
			send_loop_messages(user, type_message='keywords', context = 'help')
		elif 'contacto' in message_lower:
			send_loop_messages(user, type_message='develop', context = 'develop')
		elif 'imagen' in message_lower:
			send_loop_messages(user, type_message='image', context='common')
		elif 'video' in message_lower:
			send_loop_messages(user, type_message='video', context='common')
		elif 'hola' in message_lower:
			send_loop_messages(user, type_message='hi', context='hi', data_model =  {'first_name': user['first_name']})
		elif 'clima' in message_lower or 'soleado' in message_lower or 'nublado' in message_lower:
			user['preferences'] = "WEATHER"
			UserModel.save(user)
			add_user_location_clima(user,user['locations']['lat'],user['locations']['lng'])
			send_loop_messages(user, type_message='Clima', context='Clima')
		elif 'hospedarme' in message_lower or 'hotel' in message_lower or 'hospedaje' in message_lower :
			user['preferences'] = "HOTEL"
			UserModel.save(user)
			send_loop_messages(user, type_message='Hotel', context='Hotel')
			add_user_location_places(user,user['locations']['lat'],user['locations']['lng'], "lodging")
		elif 'comida'  in message_lower or 'comer' in message_lower or 'almorzar' in message_lower:
			user['preferences'] = "FOOD"
			UserModel.save(user)
			send_loop_messages(user, type_message='Comida', context='Comida')
			add_user_location_places(user,user['locations']['lat'],user['locations']['lng'], "cafe")
			send_loop_messages(user, type_message='Comida1', context='Comida1')
		elif 'visitar'  in message_lower or 'turistico'  in message_lower or 'concurrido'  in message_lower:
			user['preferences'] = "TOURISM"
			UserModel.save(user)
			add_user_location_places(user,user['locations']['lat'],user['locations']['lng'], "point_of_interest")
			send_loop_messages(user, type_message='Tourist', context='Tourist')
		else:
			if not flag:
				send_loop_messages(user, type_message='not_found', context = 'not_found')

def try_send_message_dos(user, message):
	message_lower = message['text'].lower()
	topic = TopicModel.find(content=message_lower)
	message = topic['message']
	
	send_loop_messages(user, type_message = message['type'], context = message['context'])
				
def check_last_connection(user):
	now = datetime.datetime.now()
	last_message = user.get('last_message', now)
	
	user['last_message'] = now
	save_user_async(user)
	
	if (now - last_message).seconds >= MAX_TIME:
		programming_message(user)
		send_loop_messages(user, type_message='specific', context = 'return_user')
		return True
	
def validate_quick_replies(user, message):
	quick_reply = message.get('quick_reply', {}) #pregunto si el mensaje tiene quick_reply
	attachments = message.get('attachments',[])
	
	if quick_reply or attachments: #si es asi ejecuto la funcion set_user_reply
		if quick_reply:
			set_user_reply(user, quick_reply)
		elif attachments:
			set_user_attachments(user, attachments)
		return True
			
def set_user_attachments(user, attachments):
	for attachment in attachments:
		if attachment['type'] == 'location':
			coordinates = attachment['payload']['coordinates']
			lat, lng = get_location(coordinates)
			if user['preferences'] == "WEATHER":
				add_user_location_clima(user,lat,lng)
				check_actions(user,'location')
			elif user['preferences'] == "TOURISM":
				add_user_location_places(user,lat,lng, "point_of_interest")
				check_actions(user,'location')
			elif user['preferences'] == "FOOD":
				add_user_location_places(user,lat,lng, "cafe")
				check_actions(user,'location')
			elif user['preferences'] == "HOTEL":
				add_user_location_places(user,lat,lng, "lodging")
				check_actions(user,'location')
			else:
				pass
			
def get_location(coordinates):
	return coordinates['lat'], coordinates['long']
		
def set_user_reply(user, quick_reply): #obtengo la respuesta del usuario y la guardo
	if user is not None:
		payload = quick_reply['payload']
		#preferences = user.get('preferences',[]) 
		
		#if not preferences or payload not in preferences:
			#preferences.append(payload)
		
		preferences = payload
		user['preferences'] = preferences
		UserModel.save(user)
		send_loop_messages(user,'quick_replies', payload)
		
def first_step(sender_id): #funcion que se ejecuta si el usuario no esta en la base de datos
		data = call_user_API(sender_id, global_token)
		user = UserModel.new(first_name = data['first_name'], last_name = data['last_name'], #Almaceno base de datos
					gender = data['gender'], user_id = sender_id, created_at = datetime.datetime.now())
		data_model = {'first_name': data['first_name']}			
		send_loop_messages(user, 'common', 'welcome', data_model)
		
def send_loop_messages(user, type_message = '', context = '', data_model = {} ): #atrae los documentos, itera y envia mensajes
	messages = MessageModel.find_by_order(type = type_message, context = context)
	for message in messages:
				
		send_messages(user,message,data_model)
		
def send_messages(user, message, data_model): #funcion para enviar mensaje
	message = get_message_data(user, message, data_model)
	typing = create_typing_message(user)
	
	call_send_API(typing, global_token)
	call_send_API(message, global_token)
		
def get_message_data(user, message, data_model = {}):
	type_message = message['type_message']
	
	if type_message == 'text_message':
		return create_text_message(user, message, data_model)
	
	elif type_message == 'quick_replies':
		return create_quick_replies(user, message)
		
	elif type_message == 'quick_replies_location':
		return create_quick_replies_location(user, message)
	
	elif type_message == 'template':
		return create_template_message(user, message)
	
	elif type_message == 'image':
		return create_image_message(user, message)
	
	elif type_message == 'video':
		return create_video_message(user, message)
	
def add_user_location_clima(user, lat, lng):
	data_model = call_geoname_API(lat,lng, global_username)
	
	#locations = user.get('locations', [])
	#locations.append({'lat': lat, 'lng': lng, 'city': data_model['city'], 'created_at': datetime.datetime.now()}) #una lista que se guardara en la base
	locations=({'lat': lat, 'lng': lng, 'city': data_model['city'], 'created_at': datetime.datetime.now()}) #una lista que se guardara en la base
	user['locations'] = locations
	UserModel.save(user) #guardo en base de datosne
	context = user['preferences']
	send_loop_messages(user, 'specific', context, data_model) #Envio mensaje

def add_user_location_sitio(user, lat, lng):
	data_model=call_geonamePlaces_API(lat,lng, global_username)
	
	locations = user.get('locations', [])
	#locations.append({'lat': lat, 'lng': lng, 'created_at': datetime.datetime.now()}) #una lista que se guardara en la base
	locations={'lat': lat, 'lng': lng, 'created_at': datetime.datetime.now()}
	user['locations'] = locations
	UserModel.save(user) #guardo en base de datosne
	context = user['preferences']
	send_loop_messages(user, 'specific', context, data_model) #Envio mensaje
	
def add_user_location_places(user, lat,lng, type):
	
	data_model=call_places_API(lat,lng, global_username, type)
	if data_model == "ZERO_RESULTS":
		send_loop_messages(user, 'sin_ubicacion', 'sin_ubicacion')
	else:
		locations = user.get('locations', [])
		#locations.append({'lat': lat, 'lng': lng, 'created_at': datetime.datetime.now()}) #una lista que se guardara en la base
		locations={'lat': lat, 'lng': lng, 'created_at': datetime.datetime.now()}
		user['locations'] = locations
		UserModel.save(user) #guardo en base de datosne
		context = user['preferences']
		send_loop_messages(user, 'specific', context, data_model) #Envio mensaje

		
	
def check_actions(user, action):
	actions = user.get('actions', [])
	
	action_structs = {action : 'Done'}
	if action_structs not in actions:
		actions.append(action_structs)
		user['actions'] = actions
		UserModel.save(user)
		
		send_loop_messages(user, type_message = 'Done', context = action)
			
def save_user_async(user):
	def async_method(user):
		UserModel.save(user)

	async = threading.Thread(name='async_method', target= async_method, args=(user, ))
	async.start()
	
def programming_message(user):
	def send_reaminer(user):
		today = datetime.datetime.today()
		future = datetime.datetime( today.year, today.month, 31, 13, 21 )
		
		time.sleep( (future - today).seconds )
		send_loop_messages(user, type_message='remainer', context= 'remainer')

	message = threading.Thread(name='send_reaminer', target= send_reaminer, 
														args=(user, ))
	message.start()