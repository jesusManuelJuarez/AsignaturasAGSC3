class Individuo():
    fitness = 0
    asignaturas = []

    def __init__(self, id, bloque, asignaturas):
        self.id = id
        self.bloque = bloque
        self.asignaturas = asignaturas

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_bloque(self):
        return self.bloque

    def set_bloque(self, bloque):
        self.bloque = bloque

    def fitness_get(self):
        return self.fitness

    def fitness_set(self, fitness):
        self.fitness = fitness
        
    def get_asignaturas(self):
        return self.asignaturas
