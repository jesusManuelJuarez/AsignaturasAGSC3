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
    cua_lim = 15
    po = 0
    pm_i = 0.6
    pm_c = 0.5
    pm_a = 0.4
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
    materias = df["Materia"]
    seriadas = df["Seriacion"]
    materias = list(materias)
    seriadas = list(seriadas)
    

    #  CONSTRUCTOR DE LA CLASE AGS QUE SE INICIALIZA AL SER INSTANCIADA
    def __init__(self, generation, pc, pm, cu_a, matricula, asignaturas):
        # LIMPIAZA DE POBLACION DE INIVDUOS PARA CADA ITERACIÓN
        self.bloque = None
        self.pob_total.clear()
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
            print("Poblacion inicial: ", self.po)
            print("Inidivuos:")
            # for i in self.pob_total:
            #     num_cuatrimestres = len(i.get_lista_asignaturas())
            #     print(f"{i.get_lista_asignaturas()} #Cuatrimestres: {num_cuatrimestres}")
            #     self.fitness(i)
            self.selection()
            self.cross()
            self.mutates()
            self.pruning()

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

    # FUNCION PARA LA CREACION DE INDIVIDUOS
    def create_init(self):
        print("----------CREACION-------------")
        
        verificar = False
        while not verificar:
            individuo_0 = self.individuo_init()
            verificar = self.validacion(individuo_0)
        print("I0:", individuo_0.get_lista_asignaturas())
        
        iterador = 0
        self.po = random.randint(4,self.pm)
        
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
                asig_ind = pob_selec[e].get_lista_asignaturas()
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

        for individuo in pob_muta:
            prob_m_i = random.random()
            if prob_m_i < self.pm_i:
                lista_asignaturas_original = individuo.get_lista_asignaturas()
                sublistas_asignaturas = self.mutates_function(lista_asignaturas_original)
                individuo.set_lista_asignaturas(sublistas_asignaturas)
                self.fitness(individuo)
                self.pob_total.append(individuo)

    def pruning(self):
        print("-----PODA......")
        # Ordena la lista de individuos (pob total) de menor a mayoy segun su valor de aptitud (fitness)
        self.pob_total = sorted(self.pob_total, key = lambda x: x.get_fitness())
        
        indi_validos = []
        for individuo in self.pob_total:
            validar = self.validacion(individuo)
            if validar:
                self.indi_validos.append(individuo)
        
        self.pob_total.clear()
        self.pob_total = indi_validos

        # Si hay menos de 3 valores, solo elimina 1 para que se puedan seguir cruzando
        if len(self.pob_total) <= 3:
            self.pob_total.pop(0)
        # Sino, elimina a dos
        elif len(self.pob_total) > 3:
            for _ in range(2):
                self.pob_total.pop(0)

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
        periodo_inicial = self.matricula[2]
        validatiion = self.validar_part_1(self.cu_a, individuo.get_lista_asignaturas(), self.asignaturas_s, periodo_inicial)
        return validatiion  

    # VALIDA QUE LAS MATERIAS CORRESPONDAN CON EL CUATRIMESTRE Y EL PERIDO EN QUE SE PLANEAN CURSAR
    def validar_part_1(self, cuatrimestre_cursar, plan_estudio, materias_cursar, periodo_inicial):
        materias_validas = []
        periodo_aux = 0
        if periodo_inicial == 3:
            periodo_aux = 0
        else:
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
        aux_seriadas = self.seriadas[index].split("-")
        # print("Materia(s) seriadas: ", aux_seriadas)
        if (len(aux_seriadas) > 1):
            for seriada in aux_seriadas:
                if seriada in materias_cursar and seriada not in materias_validas:
                    # print(f"{seriada} aun debe cursarse")
                    return False
            return True
        if aux_seriadas[0] == "NSD":
            return True
        if aux_seriadas[0] in materias_cursar and aux_seriadas[0] not in materias_validas:
            # print(f"{aux_seriadas[0]} aun debe cursarse")
            return False
        return True
    
    def mutates_function(self, plan_academico):
        for cuatrimestre in plan_academico:
            cuatrimestre_indice = plan_academico.index(cuatrimestre)
            prom_c = random.random()
            if prom_c < self.pm_c:
                # print(f"----------Mutando cuatrimestre {cuatrimestre_indice+1}----------")
                for asignatura in cuatrimestre:
                    prom_a = random.random()
                    if prom_a < self.pm_a:
                        # print(f"----------Mutando asignatura {asignatura}----------")
                        pro_m = random.random()
                        if (pro_m < self.pm_m or cuatrimestre_indice == 0):
                            if cuatrimestre_indice != (len(plan_academico)-1):
                                index_global = self.materias.index(asignatura)
                                aux_seriadas = self.seriadas[index_global].split("-")
                                index_local_1 = cuatrimestre.index(asignatura)
                                if (aux_seriadas[0] != "NSD"):
                                    for asi_seriada in aux_seriadas:
                                        success = False
                                        able_to_insert = -1
                                        for cuatri in range(len(plan_academico)):
                                            if cuatri >= cuatrimestre_indice and asi_seriada in plan_academico[cuatri]:
                                                able_to_insert = cuatri
                                                success = True
                                        if success:
                                            if able_to_insert != cuatrimestre_indice:
                                                index_mat_sacar = plan_academico[able_to_insert].index(asi_seriada)
                                                cuatrimestre.append(plan_academico[able_to_insert][index_mat_sacar])
                                                plan_academico[able_to_insert].append(asignatura)
                                                cuatrimestre.pop(index_local_1)
                                                plan_academico[able_to_insert].pop(index_mat_sacar)
                                            else:
                                                max_index = len(plan_academico[cuatrimestre_indice + 1]) - 1
                                                index_mat_sacar = random.randint(0, max_index)
                                                plan_academico[cuatrimestre_indice + 1].append(asignatura)
                                                cuatrimestre.append(plan_academico[cuatrimestre_indice + 1][index_mat_sacar])
                                                cuatrimestre.pop(index_local_1)
                                                plan_academico[cuatrimestre_indice + 1].pop(index_mat_sacar)
                                        else:
                                            random_cuatri = random.randint((cuatrimestre_indice + 1), (len(plan_academico) - 1))
                                            max_index = len(plan_academico[random_cuatri]) - 1
                                            index_mat_sacar = random.randint(0, max_index)
                                            plan_academico[random_cuatri].append(asignatura)
                                            cuatrimestre.append(plan_academico[random_cuatri][index_mat_sacar])
                                            cuatrimestre.pop(index_local_1)
                                            plan_academico[random_cuatri].pop(index_mat_sacar)
                                else:
                                    for cuatri in range(0, len(plan_academico)):
                                        if cuatri > cuatrimestre_indice:
                                            success = False
                                            for mat in plan_academico[cuatri]:
                                                index_post = self.materias.index(mat)
                                                seriadas_post = self.seriadas[index_post].split("-")
                                                if seriadas_post[0] != "NSD" and not success:
                                                    for seriada in seriadas_post:
                                                        if not success:
                                                            if seriada in cuatrimestre:
                                                                break
                                                            plan_academico[cuatri].append(asignatura)
                                                            index_mat_sacar = plan_academico[cuatri].index(mat)
                                                            cuatrimestre.append(mat)
                                                            plan_academico[cuatri].pop(index_mat_sacar)                                
                                                            cuatrimestre.pop(index_local_1)
                                                            success = True
                        else:
                            if cuatrimestre_indice != 0:
                                index_global = self.materias.index(asignatura)
                                aux_seriadas = self.seriadas[index_global].split("-")
                                index_local_1 = cuatrimestre.index(asignatura)
                                if aux_seriadas[0] !=  "NSD":
                                    able_to_insert = []
                                    for cuatri in range(cuatrimestre_indice + 1):
                                        for seriada in aux_seriadas:   
                                            if seriada not in plan_academico[cuatri]:
                                                able_to_insert.append(cuatri)
                                            else:
                                                able_to_insert.clear()
                                    if len(able_to_insert) > 0:
                                        indice_cua_auxiliar = able_to_insert[0]
                                        if (len(plan_academico[indice_cua_auxiliar]) == 7):
                                            max_index = len(plan_academico[indice_cua_auxiliar]) - 1
                                            index_mat_sacar = random.randint(0, max_index)                                                
                                            plan_academico[indice_cua_auxiliar].append(asignatura)
                                            cuatrimestre.append(plan_academico[indice_cua_auxiliar][index_mat_sacar])
                                            cuatrimestre.pop(index_local_1)
                                            plan_academico[indice_cua_auxiliar].pop(index_mat_sacar)
                                        else:
                                            plan_academico[indice_cua_auxiliar].append(asignatura)                       
        return plan_academico


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

    def view_table(self):
        indiv_m = self.pob_total[len(self.pob_total)-1]
        asig_ind = indiv_m.get_lista_asignaturas()
        lim_cu = len(asig_ind) + self.cu_a

        print("MUESTRA TABLA GRAFICAMENTE")
        df = pd.DataFrame(
            asig_ind,
            columns = ('Cuatrimestre %d' % i for i in range(self.cu_a, lim_cu)))
        # IMPRIME LA TABLA
        st.table(df)

    def view_grafica(self):
        print("MUESTRA LA GRAFICA VISUALMENTE")
