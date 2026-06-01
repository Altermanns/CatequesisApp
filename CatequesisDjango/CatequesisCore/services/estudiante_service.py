from .repositories import EstudianteRepository, SacramentoRepository

class EstudianteService:
    def __init__(self):
        self.repository = EstudianteRepository()
        self.sacramento_repo = SacramentoRepository()

    def obtener_todos(self):
        return self.repository.get_all()

    def obtener_por_id(self, id):
        return self.repository.get_by_id(id)

    def crear_estudiante(self, data):
        return self.repository.insert(data)

    def actualizar_estudiante(self, id, data):
        return self.repository.update(id, data)

    def eliminar_estudiante(self, id):
        return self.repository.delete(id)

    def buscar_por_nombre(self, nombre):
        query = {"nombre": {"$regex": nombre, "$options": "i"}}
        return self.repository.find(query)

    def obtener_sacramentos(self):
        return self.sacramento_repo.get_all()
