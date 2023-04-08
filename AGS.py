from Individuo import *
import random
import sys
import pandas as pd
import streamlit as st
import itertools

class AGS(object):
    # ATRIBUTOS PROPIOS DE CLASE
    num_generation = 0
    asignaturas_s = []
    pob_asig = []
    pob_selec = []
    pob_cruza = []
    pob_muta = []
    pob_total = []
    univer_mg = []
    pob_children = []
    cua_lim = 15
    po = 0
    pm_i = 0.6
    pm_c = 0.5
    pm_a = 0.5
    pm_m = 0.35
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

    # Cargamos el archivo CSV en un DataFrame
    df = pd.read_csv("./Plan de Estudios.csv")

    # Extraemos la columna "Model" y eliminamos los valores duplicados
    materias = df["MATERIA"]
    seriacionE = df["SERIACIONE"]
    seriacionL = df["SERIACIONL"]
    materias = list(materias)
    seracion_earlier = list(seriacionE)
    seracion_later = list(seriacionL)
    

    #  CONSTRUCTOR DE LA CLASE AGS QUE SE INICIALIZA AL SER INSTANCIADA
    def __init__(self, generation, pc, pm, cu_a, matricula, asignaturas):
        # LIMPIAZA DE POBLACION DE INIVDUOS PARA CADA ITERACIÓN
        self.bloque = None
        self.pob_total.clear()
        self.pob_selec.clear()
        self.pob_asig.clear()
        self.pob_cruza.clear()
        self.pob_muta.clear()
        # PARARAMETROS DE LA INTERFAZ GRAFICA
        self.generation = generation
        self.pc = pc
        self.pm = pm
        self.cu_a = cu_a
        self.matricula = str(matricula)
        self.asignaturas = asignaturas
        
        if self.matricula[2] != "1" and self.matricula[2] != "3":
            print("Matricula invalida: ", self.matricula)
            sys.exit(1)

        # EJECUTA HASTA EL NUMERO DE GENERACIONES ASIGNADAS EN generation
        self.create_init()
        self.ajuste()
        while True:
            # IMPLEMETANCION DE METODOS AGS
            self.print_info()
            self.selection()
            self.cross()
            self.mutates()
            self.pruning()
            self.cleaning_arrays()

            # MUESTRA EL MEJOR INDIVUDIO
            st.write("Trayectoria a seguir:")
            self.view_table()
            # CONTAR PARA CONTAR NUMERO DE CICLOS
            self.num_generation += 1
            # CONDIIONAL PARA DETENER CICLO CUANDO SEA IGUAL A generation
            if self.num_generation == generation:
                # TEST PRINT
                self.print_test()
                
                break
        
        print("FINALIZO")

    # FUNCION PARA LA CREACION DE INDIVIDUOS
    def create_init(self):
        print("----------CREACION-------------")
        
        verificar = False
        # Imprimir como se ve la estrutura de un individuo
        while not verificar:
            individuo_0 = self.individuo_init()
            verificar = self.validacion(individuo_0)
        print("I0:", individuo_0.get_lista_asignaturas())
        
        iterador = 0
        self.po = random.randint(6,self.pm)
        
        print("-------Creando a los individuos-------")
        # CLICLO PARA ITERAR Y CREAR LOS INDIVDUOS PRINCIPALES
        while iterador < self.po:
            # CARGANDO LOS ATRIBUTOS DE CADA INDIVIDUO
            id_i = len(self.pob_total)
            
            individuo_0 = self.individuo_init()
            lista_asignaturas_original = individuo_0.get_lista_asignaturas()
                
            # CREAR UN ARREGLO DE ASIGNATURAS MUTADO DEL INDIVIDUO 0
            sublistas_asignaturas = self.mutates_function(lista_asignaturas_original)
            # CREACION DE INDIVIDUO
            individuo = Individuo(id_i, self.bloque, sublistas_asignaturas)
            
            # AGREGAR A POB_TOTAL QUE CONTIENE A LA POB. DE INDIVIDUOS
            self.pob_total.append(individuo)
            
            #VERIFICAR QUE EL INDIVIDUO SEA VALIDO
            verificar = self.validacion(individuo)
            if not verificar:
                self.pob_total.pop()
                iterador -= 1
            iterador += 1
    
    def cleaning_arrays(self):
        self.pob_selec = []
        self.pob_asig = []
        self.pob_cruza = []
        self.pob_muta = []
        self.pob_children = []
    
    def print_info(self):
        print("_" * 50)
        print(f"GENERACION: {self.num_generation}")
        print("Poblacion inicial: ", self.po)
        print("Poblacion Total:", len(self.pob_total))
        for i in self.pob_total:
            num_cuatrimestres = len(i.get_lista_asignaturas())
            print(f"{i.get_lista_asignaturas()} #Cuatrimestres: {num_cuatrimestres}")
            self.fitness(i)
        for i in range(len(self.pob_total)):
            print(f"Individuo {i} Fitness: {self.pob_total[i].get_fitness()}")

    def individuo_init(self):
        self.asignaturas_s = sorted(self.asignaturas.split(","))
        self.bloque = self.cua_lim - self.cu_a
        
        aux_1, aux_2, aumento = len(self.asignaturas_s) / 7, round(len(self.asignaturas_s) / 7), 0
        if ((aux_1 - (aux_2-1)) > 1.1):
            aumento = 1
        min_divisiones = (aux_2 + aumento) # ejemplo, se puede ajustar a cualquier número
        max_divisiones = self.bloque
        # generar un número aleatorio de divisiones
        cantidad_cuatrimestres = random.randint(min_divisiones, max_divisiones)
        materia_cuatri = 0

        # dividir la lista original en N cantidad de cuatrimestres
        sublists = []
        start = 0
        for i in range(cantidad_cuatrimestres):
            if cantidad_cuatrimestres == min_divisiones:
                materia_cuatri = 7
            elif i == 0:
                materia_cuatri = random.randint(1, 7)
            elif (div_restantes == min_aux):
                materia_cuatri = 7
            else:
                materia_cuatri = random.randint(1, 7)
                
            materias_iniciales = len(self.asignaturas_s) - len(list(itertools.chain.from_iterable(sublists)))
            
            if materias_iniciales == 0:
                break
            end = start + materia_cuatri
            if end > len(self.asignaturas_s):
                end = len(self.asignaturas_s)
            sublists.append(self.asignaturas_s[start:end])
            start = end
            
            materias_restantes = len(self.asignaturas_s) - len(list(itertools.chain.from_iterable(sublists)))
            div_restantes = cantidad_cuatrimestres - (i + 1)
            aux_1, aux_2, aumento = materias_restantes / 7, round(materias_restantes / 7), 0
            if ((aux_1 - (aux_2-1)) > 1.1):
                aumento = 1
            min_aux = (aux_2 + aumento)
        indiv_init = Individuo(-1, self.bloque, sublists)
        return indiv_init

    def ajuste(self):
        cantidad_max = len(self.pob_total[0].get_lista_asignaturas())
        for i in self.pob_total:
            if len(i.get_lista_asignaturas()) > cantidad_max:
                cantidad_max = len(i.get_lista_asignaturas())
                
        for individuo in self.pob_total:
            asignatutras_aux = individuo.get_lista_asignaturas()
            for cuatri in asignatutras_aux:
                if len(cuatri) == 0:
                    index_cuatri = asignatutras_aux.index(cuatri)
                    asignatutras_aux.pop(index_cuatri)
            individuo.set_lista_asignaturas(asignatutras_aux)
            self.fitness(individuo)
            
        for i in self.pob_total:
            asignatutras_aux = []
            if len(i.get_lista_asignaturas()) < cantidad_max:
                cant_faltante = cantidad_max - len(i.get_lista_asignaturas())
                asignatutras_aux = i.get_lista_asignaturas()
                for _ in range(cant_faltante):
                    asignatutras_aux.append([])
                i.set_lista_asignaturas(asignatutras_aux)
                self.fitness(i)

    # FUNCION PARA SELECCION A LOS INVIDUOS QUE PASARAN A PROCESO DE CRUZA |PC|
    def selection(self):
        print("---------INDIVIDUOS SELECCIONADOS-------")
        # SELECCION DE INDIVIDUOS USANDO PROBABILIDAD
        list_index_repeated = []
        while True:
            for i in range(len(self.pob_total)):
                value = random.uniform(0, 0.9)

                if value <= self.pc:
                    if i not in list_index_repeated:
                        indv = self.pob_total[i]
                        self.pob_selec.append(indv)
                        list_index_repeated.append(i)

            if len(self.pob_selec) % 2 == 0 and len(self.pob_selec) != 0:
                break
            if len(self.pob_selec) == len(self.pob_total):
                list_index_repeated = []
                self.pob_selec = []
        for individuo in self.pob_selec:
            print(individuo.get_lista_asignaturas())

    # FUNCION PARA LA CRUZA
    def cross(self):
        print(".........CRUZA.........")
        pob_selec = self.pob_selec

        asignaturas_s = self.materias
        bloque = len(self.pob_selec[0].get_lista_asignaturas())

        # INDIVIDUOS ORIGINALES CRUZADOS
        print(len(self.pob_selec))
        print("-----ANTES DE CRUZA--------")
        for g in range(len(pob_selec)):
            print(pob_selec[g].get_lista_asignaturas())

        print("-------------")
        # SE ITERA EN LA POBLACION SELECCIONADA A CRUZA
        for i in range(len(pob_selec) - 1):
            asig_c = []
            asig_ind = pob_selec[i].get_lista_asignaturas()
            asig_ind_af = pob_selec[i+1].get_lista_asignaturas()
            # SE ITERA EN CADA BLOQUE DE LA POB SELECCIONA A CRUZA
            for e in range(bloque):
                asig_c.append(asig_ind[e] + asig_ind_af[e])
                # indiv_d.append(pob_selec[i+1][e] + pob_selec[i][e])

            # CREACION DE INDIVODUO
            print(asig_c)
            print("linea segun lista")
            print(list(asig_c))
            individuo = Individuo(id, self.bloque, asig_c)
            individuo.set_fitness(self.fitness(individuo))
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
                asig_ind = self.pob_cruza[e].get_lista_asignaturas()
                cont = 0
                # SE ITERA POR CADA BLOQUE DE LOS INDIVIDUOS EN LA POB_CRUZA
                for i in range(len(asig_ind)):

                    print("--------------")
                    # SE ITERA POR CADA ASIGNATURA EN LOS BLOQUES DE CADA INDIVDUO EN LA POB_CRUZA
                    for o in range(len(asig_ind[i])):
                        # SE BUSCA LA ASIGNATURA
                        value = asignaturas_s[search] == asig_ind[i][o]
                        # SI SE ENCUENTRA ENTONCES SE SUMA +1
                        if value:
                            cont += 1
                            # SE OBTIENE EL INDEX DONDE SE ENCONTRO $ SE USA TRY YA QUE SINO ENCUENTRA ENTONCES
                            # CAUSA EXCEPCION
                            try:
                                index = asig_ind[i].index(asignaturas_s[search])
                                print("index", index)
                            except:
                                print("index = none")
                        print("cont", cont)
                    # SI HAY MAS DE UNA ASIGNATURA, ES DECIR "REPETIDOS" ENTONCES ELIMINA Y DECREMENTA EL CONTADOR
                    if cont > 1:
                        asig_ind[i].pop(index)
                        cont += -1
                        print("borrar")
                # SE ACTUALIZA LA POB_CRUZA
                self.pob_cruza[e].set_lista_asignaturas(asig_ind)

        # AGREGANDO DE POB_CRUZA A POB_TOTAL
        for w in range(len(self.pob_cruza)):
            self.pob_cruza[w].set_id(len(self.pob_total))
            self.pob_muta.append(self.pob_cruza[w])

        print("-----DESPUES DE CRUZA--------")
        print("pob en cruza:", len(self.pob_cruza))
        print("pob en muta:", len(self.pob_muta))
        for q in range(len(self.pob_muta)):
            print(self.pob_muta[q].get_lista_asignaturas())

    # FUNCION PARA PROCESO DE MUTA
    def mutates(self):
        print("---------MUTA........")
        # MUTA DE INDIVIDU0OS
        pob_muta = self.pob_muta
        #SE RECORRE TODA LA POBLACION QUE SE PUEDE MUTAR
        for individuo in pob_muta:
            #GENERAMOS UN VALOR ALEATORIO ENTRE 0 Y 1
            prob_m_i = random.random()
            #VALIDAMOS SI EL INDIVIDUO MUTARA O NO
            if prob_m_i <= self.pm_i:
                #SI MUTA SE OBTENDRA SU PLAN ACADEMICO ACTUAL Y SE MANDARA A LA FUNCION DE MUTACION
                #PARA OBTENER UN NUEVO PLAN ACADEMICO
                print("I to Mutate:", individuo.get_lista_asignaturas())
                plan_academico_original = individuo.get_lista_asignaturas()
                nuevo_plan_academico_original = self.mutates_function(plan_academico_original)
                individuo.set_lista_asignaturas(nuevo_plan_academico_original)
                print("I mutated:", individuo.get_lista_asignaturas())
                self.fitness(individuo)
                self.pob_children.append(individuo)
            else:
                self.fitness(individuo)
                self.pob_children.append(individuo)

    def pruning(self):
        print("-----PODA......")
        print(f"Total de individuos antes de la PODA: {len(self.pob_total)+len(self.pob_children)}")
        indiviuos_validos = []
        for individuo in self.pob_children:
            validar = self.validacion(individuo)
            if validar:
                indiviuos_validos.append(individuo)
                
        for child in indiviuos_validos:
            self.pob_total.append(child)
        print(f"Total de individuos despues eliminar invalidos: {len(self.pob_total)}")
        
        #  SE BUSCAN INDIVIDUOS REPETIDOS PARA ELIMINARLOS
        # indiviuos_validos = []
        # plans_not_repeated = []
        
        # for individuo in self.pob_total:
        #     if individuo.get_lista_asignaturas() not in plans_not_repeated:
        #         indiviuos_validos.append(individuo)
        #         plans_not_repeated.append(individuo.get_lista_asignaturas())
        
        # if len(indiviuos_validos) >= 2:          
        #     self.pob_total.clear()
        #     self.pob_total = indiviuos_validos
        # else:        
        #     if len(self.pob_total) >= 2:
        #         value = random.randint(2, (len(self.pob_total)))
        #         for i in range(value):
        #             random_index = random.randint(0,(len(self.pob_total) - 1))
        #             if i != value:
        #                 indiviuos_validos.append(self.pob_total[random_index])
        #             else:
        #                 plan_academico_original = self.pob_total[random_index].get_lista_asignaturas()
        #                 nuevo_plan_academico_original = self.mutates_function(plan_academico_original)
        #                 self.pob_total[random_index].set_lista_asignaturas(nuevo_plan_academico_original)
        #                 self.fitness(self.pob_total[random_index])
        #                 indiviuos_validos.append(self.pob_total[random_index])
        #         self.pob_total = []
        #         self.pob_total = indiviuos_validos
        #     else:
        #         for individuo in self.pob_total:
        #             indiviuos_validos.append(individuo)
        #             plan_academico_original = individuo.get_lista_asignaturas()
        #             nuevo_plan_academico_original = self.mutates_function(plan_academico_original)
        #             individuo.set_lista_asignaturas(nuevo_plan_academico_original)
        #             self.fitness(individuo)
        #             indiviuos_validos.append(individuo)
        #         self.pob_total.clear()
        #         self.pob_total = indiviuos_validos

        # print(f"Total de individuos despues eliminar repetidos: {len(self.pob_total)}")
        
        # Ordena la lista de individuos (pob total) de menor a mayor segun su valor de aptitud (fitness)
        self.pob_total = sorted(self.pob_total, key = lambda x: x.get_fitness())

        if len(self.pob_total) >= self.pm:
            while len(self.pob_total) > self.pm:
                 self.pob_total.pop(0)
        
        # Si hay menos de 3 valores, solo elimina 1 para que se puedan seguir cruzando
        if len(self.pob_total) == 3:
            self.pob_total.pop(0)
        # Sino, elimina a dos
        elif len(self.pob_total) > 3:
            for _ in range(2):
                self.pob_total.pop(0)
        
        
        print(f"Total de individuos despues de la PODA: {len(self.pob_total)}")

    def fitness(self, individuo):
        plan_estudios = individuo.get_lista_asignaturas()
        aux_cu_a = self.cu_a
        # La lista de asignaturas debería estar estructurada de la siguiente manera:
        # N° Cuatri y Clave asignatura. p.e:
        # lista_asignaturas = [['5MDD','8IA','8CAS'],['2SAD,'5MTR'],[etc],etc]]
        aptitud_cuatri = []
        fitness = 0
        for cuatrimestre in plan_estudios:
            peso_mat_cuatri = 0
            nvl_carga = 0
            # recorre cada arreglo de la matriz (cuatrimestre)
            # cuatrimestre = ['5MDD','8IA','8CAS']
            if len(cuatrimestre) > 0:
                for asignatruas in cuatrimestre:
                    # recorre cada asignatura del cuatrismtre
                    # p.e. primero '5DD', luego '8IA', etc.
                    #calcula el peso de las materias de acuerdo a su estatus (rezagada, oridinaria, adelantada)
                    num_cuatri = asignatruas[0]
                    if int(num_cuatri) < aux_cu_a:
                        peso_mat_cuatri += (aux_cu_a - int(num_cuatri)) * 2
                    elif int(num_cuatri) == aux_cu_a:
                        peso_mat_cuatri += 1
                    else:
                        peso_mat_cuatri += (int(num_cuatri) - aux_cu_a) * 0.5
                # una vez terminado de recorrer el cuatri, multiplica el peso total de las asignaturas en el cuatri
                # por el numero de asignaturas del cuatri.
                nvl_carga = peso_mat_cuatri * len(cuatrimestre)
            aptitud_cuatri.append(nvl_carga)
            aux_cu_a += 1
        # se procede a sumar
        for f in range(len(aptitud_cuatri)-1):
            if (aptitud_cuatri[f+1] != 0):
                fitness += (aptitud_cuatri[f] - aptitud_cuatri[f+1])
        individuo.set_fitness(fitness)
        # Entre más alto el valor de fitness, mejor aptitud, por ejemplo: ;
        # ['5MDD','8IA'] = 6.5
        # ['4LSA','5DS'] = 8.5 <- Combinación más apta

    # VALIDA LAS ASIGNATURAS CON RESPECTO AL POB_ASIG
    def validacion(self, individuo):
        periodo_inicial = int(self.matricula[2])
        validatiion = self.validar_part_1(self.cu_a, individuo.get_lista_asignaturas(), self.asignaturas_s, periodo_inicial)
        return validatiion  

    # VALIDA QUE LAS MATERIAS CORRESPONDAN CON EL CUATRIMESTRE Y EL PERIDO EN QUE SE PLANEAN CURSAR
    def validar_part_1(self, cuatrimestre_cursar, plan_estudio, materias_cursar, periodo_inicial):
        materias_validas = []
        periodo_aux = 0
        if periodo_inicial == 3:
            periodo_aux = 0
        elif periodo_inicial == 1:
            periodo_aux = 1
            
        for cuatri in plan_estudio:
            # print("Cuatrimestre a cursar:\t\t", cuatrimestre_cursar)
            periodo_actual = self.cuatrimestres[cuatrimestre_cursar][periodo_aux]
            for mat in cuatri:
                # print("Materia cargada en ese cuatri: ", mat)
                num_cuatri_mate = int(mat[0])
                if (periodo_actual not in self.cuatrimestres[num_cuatri_mate]):
                    return False
                validate = self.validar_part_2(mat, materias_cursar, materias_validas)
                if not validate:
                    return False
                materias_validas.append(mat)
            cuatrimestre_cursar += 1
            # print("-"*50)
        return True

    # VALIDA QUE LAS MATERIAS CORRESPONDAN CON LA SERIACION Y SE RESPETE LA MISMA
    def validar_part_2(self, mat, materias_cursar, materias_validas):
        index = self.materias.index(mat)
        aux_seracion_earlier = self.seracion_earlier[index].split("-")
        # print("Materia(s) seriacionB: ", aux_seriacionB)
        if (len(aux_seracion_earlier) > 1):
            for seriada in aux_seracion_earlier:
                if seriada in materias_cursar and seriada not in materias_validas:
                    # print(f"{seriada} aun debe cursarse")
                    return False
            return True
        if aux_seracion_earlier[0] == "NSD":
            return True
        if aux_seracion_earlier[0] in materias_cursar and aux_seracion_earlier[0] not in materias_validas:
            # print(f"{aux_seracion_earlier[0]} aun debe cursarse")
            return False
        return True
    
    def mutates_function(self, plan_academico):
        # print("Mutates function")
        for cuatrimestre in plan_academico:
            # print(plan_academico)
            cuatrimestre_indice = plan_academico.index(cuatrimestre)
            prom_c = random.random()
            #VALIDAMOS SI EL CUATRIMESTRE MUTARA O NO
            if prom_c <= self.pm_c:
                # print(f"----------Mutando cuatrimestre {cuatrimestre_indice+1}----------")
                #SE RECORREN TODAS LA ASIGNATURAS DENTRO DEL CUATRIMESTRE
                for asignatura in cuatrimestre:
                    #SE GENERA UN VALOR ALEATORIO ENTRE 0 Y 1
                    prom_a = random.random()
                    #SE VALIDA SI LA ASIGNATURA MUTARA O NO
                    if prom_a <= self.pm_a:
                        # print(f"----------Mutando asignatura {asignatura}----------")
                        # SE GENERA UN VALOR ALEATORIO ENTRE 0 Y 1
                        pro_m = random.random()
                        # SE VALIDA SI LA ASIGNATURA SE MOVERA HACIA ADELANTE O HACIA ATRAS DEPENDIENDO DEL VALOR ALEATORIO
                        # SE GUARDA EL INDICE DE LA MATERIA EN EL CUATRIMESTRE ACTUAL
                        index_mat_local = cuatrimestre.index(asignatura)
                        # SE OBTIENE SU INDICE DE LA LISTA DE MATERIAS GENERAL
                        # PARA PODER OBTENER SUS MATERIAS ANTERIORES Y POSTERIORES SERIADAS
                        # Y UNA VARIABLE BOOLEAN PARA COMPROBAR EL ESTATUS DE SI SE REALIZO EL MOVIMIENTO
                        index_mat_general = self.materias.index(asignatura)
                        asignaturas_seriadas_earlier = self.seracion_earlier[index_mat_general].split("-")
                        asignaturas_seriadas_later = self.seracion_later[index_mat_general].split("-")
                        move_made = False
                        # SI ES EL PRIMER CUATRIMESTRE SOLO PUEDE IR HACIA ADELANTE
                        if (pro_m >= self.pm_m and cuatrimestre_indice != 0) or (cuatrimestre_indice == (len(plan_academico) - 1)):
                            print("Movimiento atras")
                            if asignaturas_seriadas_later[0] != "NSD":
                                # SE INICIALIZAN DOS VARIABLES QUE GUARDAN EL ESTADO, SI ES POSIBLE O NO MOVER LA ASIGNATURA
                                # EL MAXIMO CUATRIMESTRE DISPONIBLE PARA MOVERSE (DADO POR LA ASIGNATURA SERIADA ANTERIOR)
                                # Y A QUE POSICION SE PODRIA MOVER
                                able_to_swap = False
                                index_cuatri_to_swap = -1   
                                index_mat_to_swap = -1
                                max_index_cuatri = -1
                                # SI LA SERIACION ANTERIOR A LA ASIGNATURA NO ES UN NSD (NO SERIADA), BUSCARA
                                # EL INDICE DEL MAXIMO CUATRIMESTRE EN EL QUE PUEDE BUSCAR PARA HACER EL
                                # INTERCAMBIO SIN AFETAR LA SERIACION
                                if asignaturas_seriadas_earlier[0] != "NSD":
                                    for index_cuatri in range(len(plan_academico)):
                                        if index_cuatri <= cuatrimestre_indice:
                                            for asig_seriad in asignaturas_seriadas_earlier:
                                                if asig_seriad in plan_academico[index_cuatri]:
                                                    max_index_cuatri = index_cuatri
                                # SE RECORRE EL PLAN ACADEMICO A PARTIR DEL CUATRIMESTRE MAXIMO EN EL QUE PUEDE BUSCAR                            
                                for index_cuatri in range(len(plan_academico)):
                                    if index_cuatri <= cuatrimestre_indice and index_cuatri > max_index_cuatri:
                                        # SE RECORRE LAS ASIGNATURAS SERIADAS POSTERIORES A LA ASIGNATURA ACTUAL
                                        for mat_seriada in asignaturas_seriadas_later:
                                            # SI ALGUNA DE LAS ASIGNATURAS SERIADAS POSTERIORES A LA ASIGNATURA ACTUAL SE ENCUENTRA
                                            # EN ALGUN CUATRIMESTRE ANTERIOR AL ACTUAL
                                            if mat_seriada in plan_academico[index_cuatri]:
                                                # SE GUARDA LA INFORMACION DEL INDICE DE ESE CUATRIMESTRE DENTRO DEL PLAN ACADEMICO
                                                # Y EL INDICE DE LA ASIGNATURA SERIADA
                                                able_to_swap = True
                                                index_cuatri_to_swap = index_cuatri
                                                index_mat_to_swap = plan_academico[index_cuatri].index(mat_seriada)
                                # SE VALIDA SI ES POSBILE HACER EL INTERCAMBIO, SIEMPRE Y CUANDO EL CUATRIMESTRE HABILITADO NO SEA EL ACTUAL
                                if able_to_swap and index_cuatri_to_swap != cuatrimestre_indice:
                                    # SI ES VALIDO, SE HACE EL INTERCAMBIO DE ASIGNATURAS Y ACTUALIZA EL ESTATUS DEL MOVIMIENTO
                                    cuatrimestre.append(plan_academico[index_cuatri_to_swap][index_mat_to_swap])
                                    plan_academico[index_cuatri_to_swap].append(asignatura)
                                    cuatrimestre.pop(index_mat_local)
                                    plan_academico[index_cuatri_to_swap].pop(index_mat_to_swap)
                                    move_made = True
                            # SE VALIDA SI EL MOVIMIENTO NO SE HA HECHO (PORQUE NO ENCONTRO ASIGNATURAS SERIADAS POSTERIORES
                            # EN CUATRIMESTRES ANTERIORES, O PORQUE ES UN NSD) 
                            if not move_made:
                                # SI NO SE HA HECHO EL MOVIMIENTO INTENTARA INSERTAR LA ASIGNATURA
                                # PRIMERO SE BUSCARA SI UNA ASIGNATURA SERIADA ANTERIOR A LA ASIGNATURA ACTUAL
                                # SE ENCUENTRA EN EN CUATRIMESTRES ANTERIORES
                                able_to_insert = False
                                find_asignatura = False
                                index_cuatri_to_insert = -1
                                index_cuatri_asig_seriada = -1
                                # SE COMPRUEBA SI EXITEN ASIGNATURAS SERIADAS ANTERIORES A LA ASIGNATURA
                                if asignaturas_seriadas_earlier[0] != "NSD":
                                    # SI HAY ASIGNATURAS SERIADAS SE BUSCA LA MEJOR POSICION
                                    for index_cuatri in range(len(plan_academico)):
                                        if index_cuatri <= cuatrimestre_indice:
                                            for mat_seriada in asignaturas_seriadas_earlier:
                                                if mat_seriada in plan_academico[index_cuatri]:
                                                    index_cuatri_asig_seriada = index_cuatri
                                                    find_asignatura = True
                                                    if index_cuatri_asig_seriada < (cuatrimestre_indice - 1):
                                                        index_cuatri_to_insert = index_cuatri_asig_seriada + 1
                                                    break
                                            if find_asignatura:
                                                if index_cuatri_to_insert != -1:
                                                    able_to_insert = True
                                                break
                                else:
                                    index_cuatri_to_insert = 0
                                    able_to_insert = True
                                # SE VALIDA SI EXISTE UNA ASIGNATURA SERIADA POSTERIOR, Y SI ES POSIBLE HACER LA INSERSION
                                if able_to_insert:
                                    # SE VALIDA SI ES POSIBLE INSERTAR LA ASIGNATURA EN EL CUATRIMESTRE INDICADO
                                    validate = False
                                    for cuatri in range(len(plan_academico)):
                                        if cuatri >= index_cuatri_to_insert and cuatri < cuatrimestre_indice and len(plan_academico[cuatri]) < 7:
                                            aux_plan_academico = copy.deepcopy(plan_academico)
                                            aux_plan_academico[cuatri].append(asignatura)
                                            aux_plan_academico[cuatrimestre_indice].pop(index_mat_local)
                                            individuo_aux = Individuo(random.randint(100,1000), self.bloque, aux_plan_academico)
                                            validate = self.validacion(individuo_aux)
                                            if validate:
                                                plan_academico[cuatri].append(asignatura)
                                                cuatrimestre.pop(index_mat_local)
                                                move_made = True
                                                break
                                            else:
                                                aux_plan_academico = []
                                    if not move_made:
                                        validate = False
                                        # SI NO ES POSIBLE, TRATARA DE INTERCAMBIARALA CON ALGUNA DE LAS ASIGNATURAS
                                        # ENTRE EL CUATRIMESTRE EL CUATRIMESTRE INDICADO PARA LA INSERSION Y EL ANTERIOR AL ACTUAL
                                        for cuatri in range(len(plan_academico)):
                                            if cuatri < cuatrimestre_indice and cuatri >= index_cuatri_asig_seriada:
                                                for mat in plan_academico[cuatri]:
                                                    # SE HACE UNA COPIA DEL PLAN ACADEMICO ACTUAL, PARA REALIZAR LAS VALIDACIONES 
                                                    # EN ESTE PLAN ACADEMICO AUXILIAR
                                                    aux_plan_academico = copy.deepcopy(plan_academico)
                                                    # SE REALIZA EL INTERCAMBIO SOBRE EL PLAN ACADEMICO AUXILIAR
                                                    index_mat_to_swap = aux_plan_academico[cuatri].index(mat)
                                                    aux_plan_academico[cuatrimestre_indice].append(mat)
                                                    aux_plan_academico[cuatri].append(asignatura)
                                                    aux_plan_academico[cuatrimestre_indice].pop(index_mat_local)
                                                    aux_plan_academico[cuatri].pop(index_mat_to_swap)
                                                    individuo_aux = Individuo(random.randint(100,1000), self.bloque, aux_plan_academico)
                                                    validate = self.validacion(individuo_aux)
                                                    # SE VALIDA SI EL INTERCAMBIO DE ASIGNATURAS ES VALIDO COMO UN PLAN ACADEMICO
                                                    if validate:
                                                        # SI ES VALIDO, REALIZARA EL INTERCAMBIO EN EL PLAN ACADEMICO REAL
                                                        plan_academico[cuatrimestre_indice].append(mat)
                                                        plan_academico[cuatri].append(asignatura)
                                                        plan_academico[cuatrimestre_indice].pop(index_mat_local)
                                                        plan_academico[cuatri].pop(index_mat_to_swap)
                                                        break
                        # SI ES EL ULTIMO CUATRIMESTRE SOLO PUEDE IR HACIA ATRAS
                        elif (cuatrimestre_indice < (len(plan_academico) - 1)):
                            print("Movimiento adelante")
                            if asignaturas_seriadas_earlier[0] != "NSD":
                                # SE INICIALIZAN DOS VARIABLES QUE GUARDAN EL ESTADO, SI ES POSIBLE O NO MOVER LA ASIGNATURA
                                # EL MAXIMO CUATRIMESTRE DISPONIBLE PARA MOVERSE (DADO POR LA ASIGNATURA SERIADA POSTERIOR)
                                # Y A QUE POSICION SE PODRIA MOVER
                                able_to_swap = False
                                index_cuatri_to_swap = -1   
                                index_mat_to_swap = -1
                                max_index_cuatri = len(plan_academico)
                                # SI LA SERIACION POSTERIOR A LA ASIGNATURA NO ES UN NSD (NO SERIADA), BUSCARA
                                # EL INDICE DEL MAXIMO CUATRIMESTRE EN EL QUE PUEDE BUSCAR PARA HACER EL
                                # INTERCAMBIO SIN AFETAR LA SERIACION
                                if asignaturas_seriadas_later[0] != "NSD":
                                    for index_cuatri in range(len(plan_academico)):
                                        if index_cuatri > cuatrimestre_indice:
                                            for asig_seriad in asignaturas_seriadas_later:
                                                if asig_seriad in plan_academico[index_cuatri]:
                                                    max_index_cuatri = index_cuatri
                                # SE RECORRE EL PLAN ACADEMICO A PARTIR DEL CUATRIMESTRE QUE SE ESTA EVALUANDO ACTUALMENTE                             
                                for index_cuatri in range(len(plan_academico)):
                                    if index_cuatri >= cuatrimestre_indice and index_cuatri < max_index_cuatri:
                                        # SE RECORRE LAS ASIGNATURAS SERIADAS ANTERIORES A LA ASIGNATURA ACTUAL
                                        for mat_seriada in asignaturas_seriadas_earlier:
                                            # SI ALGUNA DE LAS ASIGNATURAS SERIADAS ANTERIORES A LA ASIGNATURA ACTUAL SE ENCUENTRA
                                            # EN ALGUN CUATRIMESTRE POSTERIOR AL ACTUAL
                                            if mat_seriada in plan_academico[index_cuatri]:
                                                # SE GUARDA LA INFORMACION DEL INDICE DE ESE CUATRIMESTRE DENTRO DEL PLAN ACADEMICO
                                                # Y EL INDICE DE LA ASIGNATURA SERIADA
                                                able_to_swap = True
                                                index_cuatri_to_swap = index_cuatri
                                                index_mat_to_swap = plan_academico[index_cuatri].index(mat_seriada)
                                # SE VALIDA SI ES POSBILE HACER EL INTERCAMBIO, SIEMPRE Y CUANDO EL CUATRIMESTRE HABILITADO NO SEA EL ACTUAL
                                if able_to_swap and index_cuatri_to_swap != cuatrimestre_indice:
                                    # SI ES VALIDO, SE HACE EL INTERCAMBIO DE ASIGNATURAS Y ACTUALIZA EL ESTATUS DEL MOVIMIENTO
                                    cuatrimestre.append(plan_academico[index_cuatri_to_swap][index_mat_to_swap])
                                    plan_academico[index_cuatri_to_swap].append(asignatura)
                                    cuatrimestre.pop(index_mat_local)
                                    plan_academico[index_cuatri_to_swap].pop(index_mat_to_swap)
                                    move_made = True
                            # SE VALIDA SI EL MOVIMIENTO NO SE HA HECHO (PORQUE NO ENCONTRO ASIGNATURAS SERIADAS ANTERIORES
                            # EN CUATRIMESTRES POSTERIORES, O PORQUE ES UN NSD) 
                            if not move_made:
                                # SI NO SE HA HECHO EL MOVIMIENTO INTENTARA INSERTAR LA ASIGNATURA
                                # PRIMERO SE BUSCARA SI UNA ASIGNATURA SERIADA POSTERIOR A LA ASIGNATURA ACTUAL
                                # SE ENCUENTRA EN EN CUATRIMESTRES POSTERIORES
                                able_to_insert = False
                                find_asignatura = False
                                index_cuatri_to_insert = -1
                                index_cuatri_asig_seriada = -1
                                # SE COMPRUEBA SI EXITEN ASIGNATURAS SERIADAS POSTERIORES A LA ASIGNATURA
                                if asignaturas_seriadas_later[0] != "NSD":
                                    # SI HAY ASIGNATURAS SERIADAS SE BUSCA LA MEJOR POSICION
                                    for index_cuatri in range(len(plan_academico)):
                                        if index_cuatri > cuatrimestre_indice:
                                            for mat_seriada in asignaturas_seriadas_later:
                                                if mat_seriada in plan_academico[index_cuatri]:
                                                    index_cuatri_asig_seriada = index_cuatri
                                                    find_asignatura = True
                                                    if index_cuatri_asig_seriada > (cuatrimestre_indice + 1):
                                                        index_cuatri_to_insert = cuatrimestre_indice + 1
                                                    break
                                            if find_asignatura:
                                                if index_cuatri_to_insert != -1:
                                                    able_to_insert = True
                                                break
                                else:
                                    index_cuatri_to_insert = len(plan_academico) - 1
                                    able_to_insert = True
                                # SE VALIDA SI EXISTE UNA ASIGNATURA SERIADA POSTERIOR, Y SI ES POSIBLE HACER LA INSERSION
                                if able_to_insert:
                                    # SE VALIDA SI ES POSIBLE INSERTAR LA ASIGNATURA EN EL CUATRIMESTRE INDICADO
                                    validate = False
                                    for cuatri in range(len(plan_academico)):
                                        if cuatri >= index_cuatri_to_insert and cuatri < index_cuatri_asig_seriada and len(plan_academico[cuatri]) < 7:
                                            aux_plan_academico = copy.deepcopy(plan_academico)
                                            aux_plan_academico[cuatri].append(asignatura)
                                            aux_plan_academico[cuatrimestre_indice].pop(index_mat_local)
                                            individuo_aux = Individuo(random.randint(100,1000), self.bloque, aux_plan_academico)
                                            validate = self.validacion(individuo_aux)
                                            if validate:
                                                plan_academico[cuatri].append(asignatura)
                                                cuatrimestre.pop(index_mat_local)
                                                move_made = True
                                                break
                                            else:
                                                aux_plan_academico = []
                                    if not move_made:
                                        validate = False
                                        # SI NO ES POSIBLE, TRATARA DE INTERCAMBIARALA CON ALGUNA DE LAS ASIGNATURAS
                                        # ENTRE EL CUATRIMESTRE POSTERIOR AL ACTUAL Y EL CUATRIMESTRE INDICADO PARA LA INSERSION
                                        for cuatri in range(len(plan_academico)):
                                            if cuatri > cuatrimestre_indice and cuatri <= index_cuatri_asig_seriada:
                                                for mat in plan_academico[cuatri]:
                                                    # SE HACE UNA COPIA DEL PLAN ACADEMICO ACTUAL, PARA REALIZAR LAS VALIDACIONES 
                                                    # EN ESTE PLAN ACADEMICO AUXILIAR
                                                    aux_plan_academico = copy.deepcopy(plan_academico)
                                                    # SE REALIZA EL INTERCAMBIO SOBRE EL PLAN ACADEMICO AUXILIAR
                                                    index_mat_to_swap = aux_plan_academico[cuatri].index(mat)
                                                    aux_plan_academico[cuatrimestre_indice].append(mat)
                                                    aux_plan_academico[cuatri].append(asignatura)
                                                    aux_plan_academico[cuatrimestre_indice].pop(index_mat_local)
                                                    aux_plan_academico[cuatri].pop(index_mat_to_swap)
                                                    individuo_aux = Individuo(random.randint(100,1000), self.bloque, aux_plan_academico)
                                                    validate = self.validacion(individuo_aux)
                                                    # SE VALIDA SI EL INTERCAMBIO DE ASIGNATURAS ES VALIDO COMO UN PLAN ACADEMICO
                                                    if validate:
                                                        # SI ES VALIDO, REALIZARA EL INTERCAMBIO EN EL PLAN ACADEMICO REAL
                                                        plan_academico[cuatrimestre_indice].append(mat)
                                                        plan_academico[cuatri].append(asignatura)
                                                        plan_academico[cuatrimestre_indice].pop(index_mat_local)
                                                        plan_academico[cuatri].pop(index_mat_to_swap)
                                                        break
        return plan_academico

    # CORRECION DE LOS INDIVIDUOS
    def correccion(self):
        print("CORRECCION DE INDIVIDUOS")

    # IMPRIME LOS INDIVIDUOS QUE CONTENGA POB_TOTAL
    def print_test(self):
        # IMPRIME A LOS INDIVIDUOS PARA DESPUES
        for i in (self.pob_total):
            print("--------------------")
            print("ID:", i.get_id())
            print("BLOQUE:", i.get_bloque())
            print("ASIGNATURAS", i.get_lista_asignaturas())
            print("APTITUD", i.get_fitness())

    def view_table(self):
        indiv_m = self.pob_total[len(self.pob_total)-1]
        asig_ind = indiv_m.get_lista_asignaturas()
        lim_cu = len(asig_ind) + self.cu_a

        print("MUESTRA TABLA GRAFICAMENTE")
        df = pd.DataFrame(
            asig_ind,
            index = ('Cuatrimestre %d' % i for i in range(self.cu_a, lim_cu)))
        # IMPRIME LA TABLA
        st.table(df)
        st.write("Aptitud:",indiv_m.get_fitness())
        st.write("Generación:", self.num_generation)

    def view_grafica(self):
        print("MUESTRA LA GRAFICA VISUALMENTE")
