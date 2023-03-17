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
        #LIMPIAZA DE POBLACION DE INIVDUOS PARA CADA ITERACIÓN
        self.pob_total.clear()
        # PARARAMETROS DE LA INTERFAZ GRAFICA
        self.epoch = epoch
        self.pc = pc
        self.po = po
        self.cu_a = cu_a
        self.matricula = matricula
        self.asignaturas = asignaturas

        #EJECUTA HASTA EL NUMERO DE EPOCAS ASIGNADAS EN epoch
        while True:
            # IMPLEMETANCION DE METODOS AGS
            self.create_init()
            self.selection()
            self.cross()
            self.mutates()
            self.pruning()
            # CONTAR PARA CONTAR NUMERO DE CICLOS
            self.num_epoch += 1
            #CONDIIONAL PARA DETENER CICLO CUANDO SEA IGUAL A EPOCH
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

            # SEPARACION POR COMA DE UNA CADENA DE ASIGNATURAS
            asignaturas_s = self.asignaturas.split(",")
            random.shuffle(asignaturas_s)

            #CREACION DE INDIVODUO
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

    def fitness(self):
        print("se calcula el fitness")
    #VALIDA LAS ASIGNATURAS CON RESPECTO AL POB_ASIG
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
            print("ID:",self.pob_total[i].id)
            print("BLOQUE:", self.pob_total[i].bloque)
            print("ASIGNATURAS", self.pob_total[i].asignaturas)