from Individuo import *
import random


class AGS(object):
    # ATRIBUTOS PROPIOS DE CLASE
    num_epoch = 0
    pob_asig = []
    pob_selec = []
    pob_total = []
    univer_mg = []
    cua_lim = 15

    #  CONSTRUCTOR DE LA CLASE AGS QUE SE INICIALIZA AL SER INSTANCIADA
    def __init__(self, epoch, pc, po, cu_a, matricula, asignaturas):
        # LIMPIAZA DE POBLACION DE INIVDUOS PARA CADA ITERACIÓN
        self.pob_total.clear()
        # PARARAMETROS DE LA INTERFAZ GRAFICA
        self.epoch = epoch
        self.pc = pc
        self.po = po
        self.cu_a = cu_a
        self.matricula = matricula
        self.asignaturas = asignaturas

        # EJECUTA HASTA EL NUMERO DE EPOCAS ASIGNADAS EN epoch
        while True:
            # IMPLEMETANCION DE METODOS AGS
            self.create_init()
            self.selection()
            self.cross()
            self.mutates()
            self.pruning()
            # CONTAR PARA CONTAR NUMERO DE CICLOS
            self.num_epoch += 1
            # CONDIIONAL PARA DETENER CICLO CUANDO SEA IGUAL A EPOCH
            if self.num_epoch == epoch:
                # TEST PRINT
                self.print_test()
                break

    # FUNCION PARA LA CREACION DE INDIVIDUOS
    def create_init(self):
        print("----------CREACION-------------")

        # CLICLO PARA ITERAR Y CREAR LOS INDIVDUOS PRINCIPALES
        for i in range(self.po):
            # CARGANDO LOS ATRIBUTOS DE CADA INDIVIDUO
            id = len(self.pob_total)
            bloque = self.cua_lim - self.cu_a

            # CREAR UN ARREGLO DE ASIGNATURAS
            asignaturas = []
            # SEPARACION POR COMA DE UNA CADENA DE ASIGNATURAS
            asignaturas_s = self.asignaturas.split(",")
            random.shuffle(asignaturas_s)

            # SE AGREGA LA LISTA DE STRING Y SE CONVIERTE EN ARREGLO
            asignaturas.append(asignaturas_s)
            for i in range(1, bloque):

                # CREA UNA FILA NUEVA EN LA MATRIZ DE ARREGLOS
                asignaturas.append([])

                for r in range(int(len(asignaturas_s) / bloque)):

                    # SE AGREGA A LA UNEVA FILA PARA RELLENAR ASIGNATURAS
                    asignaturas[i].append(asignaturas[i - 1].pop())
            print(asignaturas)

            # CREACION DE INDIVODUO
            individuo = Individuo(id, bloque, asignaturas_s)

            # AGREGAR A POB_TOTAL QUE CONTIENE A LA POB. DE INDIVIDUOS
            self.pob_total.append(individuo)

    # FUNCION PARA SELECCION A LOS INVIDUOS QUE PASARAN A PROCESO DE CRUZA |PC|
    def selection(self):
        print("---------INDIVIDUOS SELECCIONADOS-------")
        # SELECCION DE INDIVIDUOS USANDO PROBABILIDAD
        list_value = []
        # CLICLO FOR PARA UN RECORRIDO POR LA CANTIDAD DE POB INICIAL.
        for i in range(self.po):
            # VALOR DE PROBALIDAD ESTABLICIDO PARA CADA INDIVIDUO
            value = random.uniform(0, 0.9)
            list_value.append(value)

            # SI CUMPLE CON LA PROBALIDAD DE CRUZA ENTONCES AGREGA EL INDIVIDUO
            if list_value[i] <= self.pc:
                indv = self.pob_total[i]
                self.pob_selec.append(indv)

    # FUNCION PARA LA CRUZA
    def cross(self):
        print(".........CRUZA.........")

    # FUNCION PARA PROCESO DE MUTA
    def mutates(self):
        print("---------MUTA........")

    def pruning(self):
        print("-----PODA......")
        # Ordena la lista de individuos (pob total) de menor a mayoy segun su valor de aptitud (fitness)
        self.pob_total = sorted(self.pob_total, key = lambda x: x.get_fitness())
        # Si hay menos de 3 valores, solo elimina 1 para que se puedan seguir cruzando
        if len(self.pob_total) <= 3:
            self.pob_total.pop(0)
        # Sino, elimina a dos
        elif len(self.pob_total) > 3:
            for _ in range(2):
                self.pob_total.pop(0)

    def fitness(self, individuo):
        print("-------Fitness........")
        # Sumatoria de cuatrimestre actual - cuatrimestre de la materia rezagada, entre la cantidad de materias rezagadas.
        fitness = 0
        plan_estudios = individuo.get_asignaturas()
        # La lista de asignaturas debería estar estructurada de la siguiente manera:
        # N° Cuatri y Clave asignatura. p.e:
        # lista_asignaturas = [['5MDD','8IA','8CAS'],['2SAD,'5MTR'],[etc],etc]
        for cuatrimestre in plan_estudios:
            aux_fitness = 0
            # recorre cada arreglo de la matriz (cuatrimestre)
            # cuatrimestre = ['5MDD','8IA','8CAS']
            for asignatruas in cuatrimestre:
                # recorre cada asignatura del cuatrismtre
                # p.e. primero '5DD', luego '8IA', etc.
                num_cuatri = asignatruas[0]
                aux_fitness += self.cu_a - num_cuatri
            # una vez terminado de recorrer el cuatri, divide entre el numero de asignaturas del cuatri.
            aux_fitness = aux_fitness / len(asignatruas)
            # se procede a sumar
            fitness += aux_fitness
        individuo.set_fitness(fitness)
        # Entre más alto el valor de fitness, mejor aptitud, por ejemplo: ;
        # ['5MDD','8IA'] = 6.5
        # ['4LSA','5DS'] = 8.5 <- Combinación más apta

    # VALIDA LAS ASIGNATURAS CON RESPECTO AL POB_ASIG
    def validacion(self):
        print("se valida la cadena")

    # CORRECION DE LOS INDIVIDUOS
    def correccion(self):
        print("CORRECCION DE INDIVIDUOS")

    # IMPRIME LOS INDIVIDUOS QUE CONTENGA POB_TOTAL
    def print_test(self):
        # IMPRIME A LOS INDIVIDUOS PARA DESPUES
        for i in range(len(self.pob_total)):
            print("--------------------")
            print("ID:", self.pob_total[i].id)
            print("BLOQUE:", self.pob_total[i].bloque)
            print("ASIGNATURAS", self.pob_total[i].asignaturas)
