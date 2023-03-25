from Individuo import *
import random
import pandas as pd


class AGS(object):
    # ATRIBUTOS PROPIOS DE CLASE
    num_generation = 0
    pob_asig = []
    pob_selec = []
    pob_cruza = []
    pob_muta = []
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
    df = pd.read_csv(".\Plan de Estudios.csv")

    # Extraemos la columna "Model" y eliminamos los valores duplicados
    materias = df["Materia"]
    seriadas = df["Seriacion"]
    materias = list(materias)
    seriadas = list(seriadas)
    

    #  CONSTRUCTOR DE LA CLASE AGS QUE SE INICIALIZA AL SER INSTANCIADA
    def __init__(self, generation, pc, po, cu_a, matricula, asignaturas):
        # LIMPIAZA DE POBLACION DE INIVDUOS PARA CADA ITERACIÓN
        self.bloque = None
        self.pob_total.clear()
        # PARARAMETROS DE LA INTERFAZ GRAFICA
        self.generation = generation
        self.pc = pc
        self.po = po
        self.cu_a = cu_a
        self.matricula = matricula
        self.asignaturas = asignaturas

        # EJECUTA HASTA EL NUMERO DE GENERACIONES ASIGNADAS EN generation
        while True:
            # IMPLEMETANCION DE METODOS AGS
            self.create_init()
            for i in self.pob_total:
                print(i.get_lista_asignaturas())
            self.selection()
            self.cross()
            self.mutates()
            self.pruning()
            # CONTAR PARA CONTAR NUMERO DE CICLOS
            self.num_generation += 1
            # CONDIIONAL PARA DETENER CICLO CUANDO SEA IGUAL A generation
            if self.num_generation == generation:
                # TEST PRINT
                self.print_test()
                break

    # FUNCION PARA LA CREACION DE INDIVIDUOS
    def create_init(self):
        print("----------CREACION-------------")
        iterador = 0

        # CLICLO PARA ITERAR Y CREAR LOS INDIVDUOS PRINCIPALES
        # while iterador < self.po:
        while iterador < self.po:
            # CARGANDO LOS ATRIBUTOS DE CADA INDIVIDUO
            id = len(self.pob_total)
            self.bloque = self.cua_lim - self.cu_a

            # CREAR UN ARREGLO DE ASIGNATURAS
            asignaturas = []
            # SEPARACION POR COMA DE UNA CADENA DE ASIGNATURAS
            asignaturas_s = self.asignaturas.split(",")
            random.shuffle(asignaturas_s)

            # SE AGREGA LA LISTA DE STRING Y SE CONVIERTE EN ARREGLO
            asignaturas.append(asignaturas_s)
            
            # Lista de sub-listas
            sublistas_asignaturas = []
            while len(asignaturas[0]) > 0 and len(sublistas_asignaturas) < self.bloque:
                # Longitud de la sub-lista actual
                sublista_len = min(len(asignaturas[0]), random.randint(3,7))
                # Seleccionar una muestra aleatoria de la lista original
                sublista = random.sample(asignaturas[0], sublista_len)
                # Eliminar los elementos seleccionados de la lista original
                asignaturas[0] = [elem for elem in asignaturas[0] if elem not in sublista]
                # Agregar la sub-lista a la lista de sub-listas
                sublistas_asignaturas.append(sublista)

            print(sublistas_asignaturas)

            # CREACION DE INDIVODUO
            individuo = Individuo(id, self.bloque, sublistas_asignaturas, asignaturas_s)
            
            # AGREGAR A POB_TOTAL QUE CONTIENE A LA POB. DE INDIVIDUOS
            self.pob_total.append(individuo)
            
            #VERIFICAR QUE EL INDIVIDUO SEA VALIDO
            verificar = self.validacion(individuo)
            if not verificar:
                self.pob_total.pop()
                iterador -= 1
            iterador += 1

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
        pob_selec = self.pob_selec

        asignaturas_s = self.materias_list
        bloque = self.bloque

        # INDIVIDUOS ORIGINALES CRUZADOS
        print("-----ANTES DE CRUZA--------")
        for g in range(len(pob_selec)):
            print(pob_selec[g])

        print("-------------")
        # SE ITERA EN LA POBLACION SELECCIONADA A CRUZA
        for i in range(len(pob_selec) - 1):
            asig_c = []
            # SE ITERA EN CADA BLOQUE DE LA POB SELECCIONA A CRUZA
            for e in range(bloque):
                asig_c.append(pob_selec[i][e] + pob_selec[i + 1][e])
                # indiv_d.append(pob_selec[i+1][e] + pob_selec[i][e])

            # CREACION DE INDIVODUO
            individuo = Individuo(id, self.bloque, asig_c)
            self.pob_cruza.append(individuo)
            # pob_cruza.append(indiv_d)

        # CORRECCION DE FALTANTES Y ELEMENTOS REPETIDOS
        # SE ITERA POR CADA ASIGNATURA NO CURSADA
        for search in range(len(asignaturas_s)):
            print("-------------------------------")
            print(asignaturas_s[search])
            index = None
            # SE ITERA POR CADA INDIVIDUO EN LA POB_CRUZA
            for e in range(len(self.pob_cruza)):
                print("---------------------")
                cont = 0
                # SE ITERA POR CADA BLOQUE DE LOS INDIVIDUOS EN LA POB_CRUZA
                for i in range(len(self.pob_cruza[e].get_asignaturas())):

                    print("--------------")
                    # SE ITERA POR CADA ASIGNATURA EN LOS BLOQUES DE CADA INDIVDUO EN LA POB_CRUZA
                    for o in range(len(self.pob_cruza[e][i].get_asignaturas())):
                        # SE BUSCA LA ASIGNATURA
                        value = asignaturas_s[search] == self.pob_cruza[e][i][o].get_asignaturas()
                        # SI SE ENCUENTRA ENTONCES SE SUMA +1
                        if value:
                            cont += 1
                            # SE OBTIENE EL INDEX DONDE SE ENCONTRO $ SE USA TRY YA QUE SINO ENCUENTRA ENTONCES
                            # CAUSA EXCEPCION
                            try:
                                index = self.pob_cruza[e][i].get_asignaturas().index(asignaturas_s[search])
                                print("index", index)
                            except:
                                print("index = none")
                        print("cont", cont)
                    # SI HAY MAS DE UNA ASIGNATURA, ES DECIR "REPETIDOS" ENTONCES ELIMINA Y DECREMENTA EL CONTADOR
                    if cont > 1:
                        self.pob_cruza[e][i].get_asignaturas().pop(index)
                        cont += -1
                        print("borrar")
        # AGREGANDO DE POB_CRUZA A POB_TOTAL
        for i in range(len(self.pob_cruza)):
            self.pob_cruza[i].set_id(len(self.pob_total))
            self.pob_muta.append(self.pob_cruza[i])

    # FUNCION PARA PROCESO DE MUTA
    def mutates(self):
        print("---------MUTA........")
        # MUTA DE INDIVIDU0OS
        pob_muta = self.pob_muta
        bloq = self.bloque

        for i in range(len(pob_muta)):
            value = ""
            for e in range(bloq - 1):
                value = pob_muta[i][e + 1].get_asignaturas().pop()
                pob_muta[i][e].get_asignaturas().append(value)
            # AGREGANDO DE POB MUTA A POB GLOBAL
            pob_muta[i].set_id(len(self.pob_total))
            self.pob_total.append(pob_muta[i])

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
        plan_estudios = individuo.get_lista_asignaturas()
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
    def validacion(self, individuo):
        validatiion = self.validar_part_1(self.cu_a, individuo.get_lista_asignaturas(), individuo.get_asignaturas_cursar())
        return validatiion  

    # VALIDA QUE LAS MATERIAS CORRESPONDAN CON EL CUATRIMESTRE Y EL PERIDO EN QUE SE PLANEAN CURSAR
    def validar_part_1(self, cuatrimestre_cursar, lista_asignaturas, materias_cursar):
        materias_validas = []
        for cuatri in lista_asignaturas:
            print("Cuatrimestre a cursar:\t\t", cuatrimestre_cursar)
            for mat in cuatri:
                print("Materia cargada en ese cuatri: ", mat)
                if mat not in materias_cursar:
                    return False
                num_cuatri_mate = mat[0]
                periodos_actuales = self.cuatrimestres[cuatrimestre_cursar]
                if (num_cuatri_mate in self.periodos[periodos_actuales[0]] and str(cuatrimestre_cursar) not in self.periodos[periodos_actuales[0]]) or (num_cuatri_mate in self.periodos[periodos_actuales[1]] and str(cuatrimestre_cursar) not in self.periodos[periodos_actuales[1]]):
                    return False
                validate = self.validar_part_2(mat, materias_cursar, materias_validas)
                if not validate:
                    return False
                materias_validas.append(mat)
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
