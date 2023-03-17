class Individuo():
    fitness = 0
    asignaturas = []

    def __init__(self, id, bloque, asignaturas):
        self.id = id
        self.bloque = bloque
        self.asignaturas = asignaturas

    def id_get(self):
        return self.id

    def id_set(self, id):
        self.id = id

    def bloque_get(self):
        return self.bloque

    def bloque_set(self, bloque):
        self.bloque = bloque

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, fitness):
        self.fitness = fitness
