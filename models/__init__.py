from pymongo import MongoClient
from user import User
from message import Message
#from topic import Topic

import json
import os

def get_path():
	return os.path.dirname( os.path.realpath(__file__))
	
def pluralize_class(instance):
	return "{class_name}s".format( class_name = instance.__class__.__name__ )

def load_data(model, folder = 'data'): #funcion para cargar los mensajes de un modelo
	path = "{path}/{folder}/{file_name}.json".format( path = get_path(),
													folder = folder, 
													file_name = pluralize_class(model) )
	with open('models/data/messages.json') as data:
		list_data = json.load(data) #parseo a json
		for json_data in list_data: #recorremos el archivo
			model.save(json_data) #insertamos base de datos
	

URL = 'localhost'
PORT = 27017
USER_COLLECTION = 'users' #Esta coleccion no esta creada
MESSAGE_COLLECTION = 'messages'
#TOPIC_COLLECTION = 'topics'

client = MongoClient(URL, PORT)
database = client.bot

UserModel = User(database, USER_COLLECTION)

MessageModel = Message(database, MESSAGE_COLLECTION)
MessageModel.delete_collection() #borra las colecciones

#TopicModel = Topic(database, TOPIC_COLLECTION)
#TopicModel.delete_collection()

load_data(MessageModel) #carga el modelo de mensajes
#load_data(TopicModel)