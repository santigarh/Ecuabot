class Model(object):
	def __init__(self, database, collection_name):
		self.database = database
		self.collection_name = collection_name
		self.collection = database[self.collection_name]
	
	def new(self, **kwargs): #guarda en la base de datos pasando varios argumentos un diccionario
		return self.save(kwargs)
		
	def  save(self, document):
		self.collection.save(document)
		return document
	
	def find(self, **kwargs): #hace una busqueda depende los argumentos que se mande
		return self.collection.find_one(kwargs)
		
	def find_all(self, **kwargs): #retorna todos los documentos de la colleccion
		return self.collection.find(kwargs)