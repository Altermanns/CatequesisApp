import os
from pymongo import MongoClient
from bson import ObjectId

class MongoConnection:
    _client = None
    _db = None

    @classmethod
    def get_db(cls):
        if cls._db is None:
            mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/Catequesis')
            cls._client = MongoClient(mongo_uri)
            # Manejo de Atlas (srv) vs Local
            if 'srv' in mongo_uri:
                cls._db = cls._client.get_default_database()
            else:
                # Extraer nombre de la DB de la URI o usar default
                cls._db = cls._client['Catequesis']
        return cls._db

class BaseMongoRepository:
    collection_name = None

    def __init__(self):
        self.db = MongoConnection.get_db()
        self.collection = self.db[self.collection_name]

    def _transform(self, data):
        if data and "_id" in data:
            data["id"] = str(data["_id"])
        return data

    def get_all(self):
        return [self._transform(item) for item in self.collection.find()]

    def get_by_id(self, id):
        return self._transform(self.collection.find_one({"_id": id}))

    def insert(self, data):
        return self.collection.insert_one(data)

    def update(self, id, data):
        return self.collection.update_one({"_id": id}, {"$set": data})

    def delete(self, id):
        return self.collection.delete_one({"_id": id})

    def find(self, query):
        return [self._transform(item) for item in self.collection.find(query)]

class CatequistaRepository(BaseMongoRepository):
    collection_name = 'Catequista'

class EstudianteRepository(BaseMongoRepository):
    collection_name = 'Estudiante'

class GrupoRepository(BaseMongoRepository):
    collection_name = 'Grupos'

class SacramentoRepository(BaseMongoRepository):
    collection_name = 'Sacramentos'

class SyncTextilRepository(BaseMongoRepository):
    collection_name = 'SyncTextil'

