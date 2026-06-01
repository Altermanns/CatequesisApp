from .repositories import CatequistaRepository

class CatequistaService:
    def __init__(self):
        self.repository = CatequistaRepository()

    def obtener_todos(self):
        return self.repository.get_all()

    def obtener_por_id(self, id):
        return self.repository.get_by_id(id)

    def crear_catequista(self, data):
        # Aquí se podrían añadir validaciones
        return self.repository.insert(data)

    def actualizar_catequista(self, id, data):
        return self.repository.update(id, data)

    def eliminar_catequista(self, id):
        return self.repository.delete(id)

    def buscar_por_nombre(self, nombre):
        query = {"nombre": {"$regex": nombre, "$options": "i"}}
        return self.repository.find(query)
