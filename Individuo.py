class Individuo():
    fitness = 0
    asignaturas = []

    def __init__(self, id, bloque, lista_asignaturas, asignaturas_cursar):
        self.id = id
        self.bloque = bloque
        self.lista_asignaturas = lista_asignaturas
        self.asignaturas_cursar = asignaturas_cursar

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_bloque(self):
        return self.bloque

    def set_bloque(self, bloque):
        self.bloque = bloque

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, fitness):
        self.fitness = fitness
        
    def get_lista_asignaturas(self):
        return self.lista_asignaturas
    
    def get_asignaturas_cursar(self):
        return self.asignaturas_cursar
