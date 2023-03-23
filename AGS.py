from Individuo import *
import random
import pandas as pd


class AGS(object):
    # ATRIBUTOS PROPIOS DE CLASE
    num_epoch = 0
    pob_asig = []
    pob_selec = []
    pob_total = []
    univer_mg = []
    cua_lim = 15
    materias_list = []
    cuatrimestres = {
        1 : [3,1],
        2 : [1,2],
        3 : [2,3],
        4 : [3,1],
        5 : [1,2],
        6 : [2,3],
        7 : [3,1],
        8 : [1,2],
        9 : [2,3],
        10 : [3,1],
        11 : [1,2],
        12 : [2,3],
        13 : [3,1],
        14 : [1,2],
    }
        
    periodos = {
        1 : ["1","2","4","5","7","8","10","13","14"],
        2 : ["2","3","5","6","8","9","11","12","14"],
        3 : ["1","3","4","6","7","9","10","12","13"]
    }

    # Cargamos el archivo CSV en un DataFrame
    df = pd.read_csv("AsignaturasAGSC3\Plan de Estudios.csv")

    # Extraemos la columna "Model" y eliminamos los valores duplicados
    materias = df["Materia"]
    seriadas = df["Seriacion"]
    materias = list(materias)
    seriadas = list(seriadas)
    

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
            for j in range(1, bloque):

                # CREA UNA FILA NUEVA EN LA MATRIZ DE ARREGLOS
                asignaturas.append([])

                for r in range(int(len(asignaturas_s) / bloque)):

                    # SE AGREGA A LA UNEVA FILA PARA RELLENAR ASIGNATURAS
                    asignaturas[j].append(asignaturas[j - 1].pop())
            print(asignaturas)

            # CREACION DE INDIVODUO
            individuo = Individuo(id, bloque, asignaturas_s)
            
            # AGREGAR A POB_TOTAL QUE CONTIENE A LA POB. DE INDIVIDUOS
            self.pob_total.append(individuo)
            
            #VERIFICAR QUE EL INDIVIDUO SEA VALIDO
            verificar = self.validacion(individuo, asignaturas)
            if not verificar:
                i -= 1
                self.pob_total.pop()

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
    def validacion(self, individuo, asignaturas):
        print("se valida la cadena")
        cuatrimestre_cursar = self.cu_a + 1

        validatiion = self.validar_part_1(self.cu_a, cuatrimestre_cursar, individuo.get_asignaturas(), asignaturas)
        return validatiion  

    # VALIDA QUE LAS MATERIAS CORRESPONDAN CON EL CUATRIMESTRE Y EL PERIDO EN QUE SE PLANEAN CURSAR
    def validar_part_1(self, cuatrimestre_anterior, cuatrimestre_cursar, lista_asignaturas, materias_cursar):
        materias_validas = []
        for cuatri in lista_asignaturas:
            print("Cuatrimestre a cursar:\t\t", cuatrimestre_cursar)
            for mat in cuatri:
                print("Materia cargada en ese cuatri: ", mat)
                if mat not in materias_cursar:
                    return False
                num_cuatri_mate = mat[0]
                if int(num_cuatri_mate) < cuatrimestre_anterior:
                    return False
                periodos_actuales = self.cuatrimestres[cuatrimestre_cursar]
                if (num_cuatri_mate in self.periodos[periodos_actuales[0]] and str(cuatrimestre_cursar) not in self.periodos[periodos_actuales[0]]) or (num_cuatri_mate in self.periodos[periodos_actuales[1]] and str(cuatrimestre_cursar) not in self.periodos[periodos_actuales[1]]):
                    return False
                validate = self.validar_part_2(mat, materias_cursar, materias_validas)
                if not validate:
                    return False
                materias_validas.append(mat[1:]) 
            cuatrimestre_cursar += 1
            print("-"*50)
        return True

    # VALIDA QUE LAS MATERIAS CORRESPONDAN CON LA SERIACION Y SE RESPETE LA MISMA
    def validar_part_2(self, mat, materias_cursar, materias_validas):
        index = self.materias.index(mat)
        aux_seriadas = []
        if (len(self.seriadas[index]) > 4):
            aux_seriadas = self.seriadas[index].split("-")
        else:
            aux_seriadas.append(self.seriadas[index])
        print("Materia(s) seriadas: ", aux_seriadas)
        if (len(aux_seriadas) > 1):
            for ser in aux_seriadas:
                if ser in materias_cursar and ser not in materias_validas:
                    print(f"{ser} aun debe cursarse")
                    return False
            return True
        if aux_seriadas[0] == "NAP":
            return True
        if aux_seriadas[0] in materias_cursar and aux_seriadas[0] not in materias_validas:
            print(f"{aux_seriadas[0]} aun debe cursarse")
            return False
        return True

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
