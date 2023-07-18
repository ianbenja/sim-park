import copy
from Clases import *
import numpy as np
import random
import math
from RK import *



# Variables de llegadas coche VIRUS
cont_llegadas = 0
cola_llegadas = 0
funciona = 'FUNCIONA'
llegada_rota = 'VIRUS'
estado_llegadas = funciona

# Parametros para Estadisticas
tiempo_permanencia_AC_boleteria = 0
cantidad_grupos_atendido_boleteria = 0
tiempo_permanencia_AC_control = 0
cantidad_grupos_atendido_control = 0

# Atencion Boleteria

cantidad_entrada_GA = 0
tiempo_entrada_PC = 0

# Control Alimentos

cantidad_alimentos_GA = 0
tiempo_alimentos_PC = 0

# Contado Sorteo

contador_sorteos = 0

# Tipo RK
llegadas_rk = "Llegadas"
servidores_rk = "Servidores"
Tipo_RK_glo = llegadas_rk

# Estados
libre = "Libre"
ocupado = "Ocupado"
siendo_atendido = "Siendo_Atendido"
esperando_atencion = "Esperando_Atencion"
sa_boleteria = "Siendo_Atendido_Boleteria"
ea_boleteria = "Esperando_Atencion_Boleteria"
sa_control = "Siendo_Atendido_Control"
ea_control = "Esperando_atencion_Control"
sorteando = "Sorteando"

# RELOJ

reloj = 0

def proximo_evento(vector):
    menor_valor = float('inf')  # Valor inicial asumido como infinito
    lugar_sublista = -1  # Variable para almacenar la posición de la sublista (-1 indica que no se encontró ninguna sublista)
    for i in range(1, 7):
        
        
        if i == 5:
            for j, atributo in enumerate(vector[i][3]):
                    if atributo is not None and atributo < menor_valor:
                        menor_valor = atributo
                        prox_evento = i
                        lugar_sublista = j

        else:

            if isinstance(vector[i][2], list):  # Comprobar si es una sublista en lugar de una tupla
                for j, atributo in enumerate(vector[i][2]):
                    if atributo is not None and atributo < menor_valor:
                        menor_valor = atributo
                        prox_evento = i
                        lugar_sublista = j
            else:
                if vector[i][2] is not None and vector[i][2] < menor_valor:
                    menor_valor = vector[i][2]
                    prox_evento = i
                    lugar_sublista = -1
    if vector[14][3] is not None and vector[14][3] < menor_valor:
        prox_evento = 14
        menor_valor = vector[14][3]
        lugar_sublista = 3
    if vector[16][2] is not None and vector[16][2] < menor_valor:
        prox_evento = 16
        menor_valor = vector[16][2]
        lugar_sublista = 2
    return prox_evento, lugar_sublista, menor_valor


def inicializacion_vector(autos,horas):
    global tiempo_permanencia_AC_boleteria
    global cantidad_grupos_atendido_boleteria
    global tiempo_permanencia_AC_control
    global cantidad_grupos_atendido_control
    global cantidad_entrada_GA
    global tiempo_entrada_PC
    global cantidad_alimentos_GA
    global tiempo_alimentos_PC
    global contador_sorteos
    global reloj
    global cont_llegadas
    global cola_llegadas
    global estado_llegadas

    reloj = 0
    cont_llegadas = 0
    cola_llegadas = 0
    tiempo_permanencia_AC_boleteria = 0
    cantidad_grupos_atendido_boleteria = 0
    tiempo_permanencia_AC_control = 0
    cantidad_grupos_atendido_control = 0
    cantidad_entrada_GA = 0
    tiempo_entrada_PC = 0
    cantidad_alimentos_GA = 0
    tiempo_alimentos_PC = 0
    contador_sorteos = 0
    estado_llegadas = funciona





    a, b, c = proximo_coche(autos,horas)
    ve = [a,b,c]
    llegadacoche = ve
    finestacionamiento = [None,None,[None,None,None,None,None]]
    llegadaboleteria = [None,None,None,0]
    finatencionboleteria = [None,None,[None,None,None,None]]
    fincontrolalimentos = [None,None,None,[None,None,None,None,None]]
    finsorteo = [None,None,None,0,None,None]
    cajasestacionamiento = [[libre, 0,[0,0]],[libre, 0,[0,0]],[libre, 0,[0,0]],[libre, 0,[0,0]],[libre, 0,[0,0]]]
    colasboleteria = [[[libre,libre],0,[0,0]],[[libre,libre],0,[0,0]]]
    controlalimento = [[libre, 0],[libre, 0],[libre, 0],[libre, 0],[libre, 0]]
    sorteo = libre
    evento_de = "Inicializacion"
    #ESTADISTICAS
    #[Cantidad boleteria] [Tiempo Boleteria] [Promedio AC] [Cantidad Control] [Tiempo Control] [Promedio AC]
    estadisticas = [0,0,0,0,0,0]
    rk1 = [None, None, None, None]
    def_tipo = [None, None]
    rk_tipo = [None, None, None]

    vector = [reloj,llegadacoche,finestacionamiento,llegadaboleteria,finatencionboleteria,fincontrolalimentos,finsorteo,cajasestacionamiento,colasboleteria,controlalimento,sorteo,estadisticas,evento_de, cont_llegadas, rk1, def_tipo, rk_tipo, cola_llegadas]
    return vector

def reemplazar_none(vector):
    for i in range(len(vector)):
        if isinstance(vector[i], list):
            reemplazar_none(vector[i])
        elif vector[i] is None:
            vector[i] = ''
    return vector

def flatten_vector(vector):
    flattened_vector = []

    def flatten_helper(element):
        if isinstance(element, (int, float, str)):
            flattened_vector.append(element)
        elif isinstance(element, list):
            for item in element:
                flatten_helper(item)

    for element in vector:
        flatten_helper(element)

    return flattened_vector


def logica_vector(autos, horas, tiempo_est, tiempo_bol, tiempo_con, tiempo_sor):
    global contador_sorteos
    global reloj
    cola_caminando = []
    # SIMULACION
    vector_data = []
    iteration_count = 0
    vector_actual = inicializacion_vector(autos, horas)
    inicial = copy.deepcopy(vector_actual)
    fin = reemplazar_none(inicial)
    fin = flatten_vector(fin)
    # actualizar_tabla(vector_actual)
    #print("ESTADO INICIAL DEL VECTOR")
    #print(vector_actual)
    #print("MODIFICADO ESTADO INICIAL DEL VECTOR")
    #print(fin)
    vector_data.append(fin)

    #Inicializacion de variables de RK
    rk1_vector_lleno = None
    rk2_vector_lleno = None
    rk3_vector_lleno = None

    #Inicializacion Vector Historial
    historial_RK = []

    # Cambio de for a while
    while vector_actual[0] <= (horas * 3600):
        evento, posicion, actualizar_reloj = proximo_evento(vector_actual)
        reloj = actualizar_reloj
        vector_actual, cola_caminando, rk1_vec,rk2_vec,rk3_vec = paso_vector(evento, posicion, actualizar_reloj, cola_caminando, vector_actual,
                                                    autos, horas, tiempo_est, tiempo_bol, tiempo_con, tiempo_sor)
        sec = copy.deepcopy(vector_actual)
        fin_2 = reemplazar_none(sec)
        fin_2 = flatten_vector(fin_2)
        fin_2[0] = np.round(fin_2[0], decimals=3)
        #print(iteration_count, "ITERACION DEL VECTOR MODIFICADA")
        #print('VECTOR FLATTEN', fin_2)
        #print('ESTE ES EL LARGO DEL FLATEN', len(fin_2))
        vector_data.append(fin_2)
        # actualizar_tabla(vector_actual)
        iteration_count += 1
        #print(iteration_count, "ITERACION DEL VECTOR")
        #print(vector_actual)

        if not rk1_vec is None:
            rk1_vector_lleno = rk1_vec
            linea_final = rk1_vec[-1]
            tiempo_min = linea_final[6]*30
            historial_RK.append(["RK Tiempo", actualizar_reloj, linea_final[8], linea_final[6], tiempo_min ,tiempo_min*60 ])


        if not rk2_vec is None:
            rk2_vector_lleno = rk2_vec
            linea_final = rk2_vec[-1]
            tiempo_min = linea_final[6] * 27
            historial_RK.append(["RK Llegadas", actualizar_reloj, None, linea_final[6], tiempo_min,
                                tiempo_min * 60])

        if not rk3_vec is None:
            rk3_vector_lleno = rk3_vec
            linea_final = rk3_vec[-1]
            tiempo_min = linea_final[6] * 8
            historial_RK.append(["RK Servicios", actualizar_reloj, None, linea_final[6], tiempo_min,
                                tiempo_min * 60])

    #print(vector_data, "VECTOR DATA")
    return vector_data, iteration_count, rk1_vector_lleno, rk2_vector_lleno, rk3_vector_lleno, historial_RK

def Limpiar_Vector(vector):
    #vector = [reloj,llegadacoche,finestacionamiento,llegadaboleteria,finatencionboleteria,fincontrolalimentos,finsorteo,cajasestacionamiento,colasboleteria,controlalimento,sorteo,estadisticas,evento_de]
    vector[1][0] = None
    vector[1][1] = None
    vector[2][0] = None
    vector[2][1] = None
    vector[3][0] = None
    vector[3][1] = None
    vector[4][0] = None
    vector[4][1] = None
    vector[5][0] = None
    vector[5][1] = None
    vector[5][2] = None
    vector[6][0] = None
    vector[6][1] = None
    vector[6][4] = None
    vector[6][5] = None
    return vector

def paso_vector(evento, posicion, actualizar_reloj, cola_caminando, vector_actual,autos, horas, tiempo_est_v, tiempo_bol_v, tiempo_con, tiempo_sor):
    vector_actual = Limpiar_Vector(vector_actual)
    rk1_vector = None
    rk_vector_2 = None
    rk_vector_3 = None

    global cola_llegadas
    global estado_llegadas

    if evento == 1 and estado_llegadas == funciona:
        # Llegada Coche
        rnd, hora_auto, prox_auto, rnd_fin, tiempo_est, fin_est, caja, promedioAC = llegada_coche(autos, horas,tiempo_est_v)
        # Hay que poner en None todos los RND antes de entrar a los IF
        # (PARA TODOS LOS POSIBLES EVENTOS)

        if not prox_auto is None:
            prox_auto = np.round(prox_auto, decimals=3)
        if not fin_est is None:
            fin_est = np.round(fin_est, decimals=3)

        pos = caja.identificador
        vector_actual[0] = actualizar_reloj
        vector_actual[1][0] = rnd
        vector_actual[1][1] = hora_auto
        vector_actual[1][2] = prox_auto
        vector_actual[2][0] = rnd_fin
        vector_actual[2][1] = tiempo_est
        if not fin_est is None:
            vector_actual[2][2][pos] = fin_est
        vector_actual[7][pos][0] = ocupado
        vector_actual[7][pos][1] = caja.obtener_largo()
        if not promedioAC is None:
            vector_actual[7][pos][2] = [actualizar_reloj, promedioAC]
        vector_actual[12] = "Llegada_Coche"
        vector_actual[13] = cont_llegadas
        if cont_llegadas == 150 and rk1_vector is None:
            rk1_vector, b = RK_1(actualizar_reloj)
            tiempo_interrup = tiempo_RK(30, rk1_vector)
            llegada_rk1 = actualizar_reloj + tiempo_interrup
            vector_actual[14][0] = actualizar_reloj
            vector_actual[14][1] = b
            vector_actual[14][2] = tiempo_interrup
            vector_actual[14][3] = llegada_rk1


    elif evento == 2:
        caja = cajas_estacionamiento[posicion]
        rnd_fin, tiempo_est, fin_est, estado, promedioAC, tiempo_cola = fin_atencion_estacionamiento(caja,tiempo_est_v)
        cuando_llega = actualizar_reloj + 300
        cola_caminando.append(cuando_llega)

        vector_actual[0] = actualizar_reloj
        vector_actual[2][0] = rnd_fin
        vector_actual[2][1] = tiempo_est
        vector_actual[2][2][posicion] = fin_est
        vector_actual[7][posicion][0] = estado
        vector_actual[7][posicion][1] = caja.obtener_largo()
        if not promedioAC is None:
            vector_actual[7][posicion][2] = [promedioAC, tiempo_cola]
        vector_actual[3][2] = cola_caminando[0]
        vector_actual[3][3] = len(cola_caminando)
        vector_actual[12] = "Fin_Estacionamiento"



    elif evento == 3:
        rnd, entrada, rnd_control, personas_control, tiempo_control, control, rnd_bol, tiempo_bol, tiempo_fin_bol, promedioAC, largo_cola_bol, caja, cola = llegada_del_estacionamiento(tiempo_bol_v,tiempo_con)
        vector_actual[0] = actualizar_reloj

        if not tiempo_fin_bol is None:
            tiempo_fin_bol = np.round(tiempo_fin_bol, decimals=3)

        if entrada:
            posicion_control = control.identicador
        else:
            if cola == -1:
                posi = caja.identificador
                if posi == 0 or posi == 2:
                    lugar_cola = 0
                elif posi == 1 or posi == 3:
                    lugar_cola = 1
                posi_cola = caja.cola.identificador
            if caja == -1:
                posi_cola = cola.identificador
            

            vector_actual[3][0] = rnd
            vector_actual[3][1] = entrada
        cola_caminando.pop(0)
        if len(cola_caminando) > 0:
            vector_actual[3][2] = cola_caminando[0]
        else:
            vector_actual[3][2] = None
        vector_actual[3][3] = len(cola_caminando)

        if entrada:
            vector_actual[5][0] = rnd_control
            vector_actual[5][1] = personas_control
            vector_actual[5][2] = tiempo_control
            if not tiempo_control is None:
                vector_actual[5][3][posicion_control] = np.round((actualizar_reloj + tiempo_control), decimals=3)

            if not vector_actual[9][posicion_control][0] == "Interrumpido":
                vector_actual[9][posicion_control][0] = ocupado


            vector_actual[9][posicion_control][1] = len(control.cola)
        else:
            if cola == -1:
                vector_actual[4][0] = rnd_bol
                vector_actual[4][1] = tiempo_bol
                vector_actual[4][2][posi] = tiempo_fin_bol
            if not tiempo_fin_bol is None:
                vector_actual[8][posi_cola][0][lugar_cola] = ocupado
                vector_actual[8][posi_cola][1] = largo_cola_bol
                if not promedioAC is None:
                    vector_actual[8][posi_cola][2] = [promedioAC, actualizar_reloj]
        vector_actual[12] = "Llegada_Boleteria"


    elif evento == 4:
        caja = cajas_boleteria[posicion]
        rnd, tiempo, tiempo_fin, promedioAC, estado, rnd_per, personas, tiempo_per, control = fin_atencion_boleteria(caja,tiempo_con, tiempo_bol_v)

        if not tiempo_fin is None:
            tiempo_fin = np.round(tiempo_fin, decimals=3)

        posi = caja.identificador
        if posi == 0 or posi == 2:
            lugar_cola = 0
        elif posi == 1 or posi == 3:
            lugar_cola = 1
        posi_cola = caja.cola.identificador
        vector_actual[0] = actualizar_reloj
        vector_actual[4][0] = rnd
        vector_actual[4][1] = tiempo
        vector_actual[4][2][posicion] = tiempo_fin
        vector_actual[8][posi_cola][0][lugar_cola] = estado
        vector_actual[8][posi_cola][1] = caja.cola.obtener_largo()
        if not promedioAC is None:
            vector_actual[8][posi_cola][2] = [promedioAC, actualizar_reloj]
        vector_actual[11][0] = cantidad_grupos_atendido_boleteria
        vector_actual[11][1] = tiempo_permanencia_AC_boleteria
        promedio_cal = np.round(tiempo_permanencia_AC_boleteria / cantidad_grupos_atendido_boleteria, decimals=3)
        vector_actual[11][2] = promedio_cal
        control_id = control.identicador

        # Si no habia cola en control alimentos
        if not rnd_per is None:
            vector_actual[5][0] = rnd_per
            vector_actual[5][1] = personas
            vector_actual[5][2] = tiempo_per
            vector_actual[5][3][control_id] = np.round((actualizar_reloj + tiempo_per), decimals=3)

        if not vector_actual[9][control_id][0] == "Interrumpido":
            vector_actual[9][control_id][0] = ocupado
        vector_actual[9][control_id][1] = len(control.cola)
        vector_actual[12] = "Fin_Boleteria"


    elif evento == 5:
        control = controles_alimentos[posicion]
        control_id = control.identicador
        rnd, personas, tiempo_per, estado, rnd_sorteo, tiempo_sorteo, tiempo_final_sorteo = fin_control_alimentos(control,tiempo_sor)
        vector_actual[0] = actualizar_reloj
        '''if not tiempo_final_sorteo is None:
            tiempo_final_sorteo = np.round(tiempo_final_sorteo, decimals=3)'''

        if not rnd is None:
            vector_actual[5][3][control_id] = np.round((actualizar_reloj + tiempo_per), decimals=3)
        else:
            vector_actual[5][3][control_id] = None

        vector_actual[5][0] = rnd
        vector_actual[5][1] = personas
        vector_actual[5][2] = tiempo_per


        vector_actual[11][3] = cantidad_grupos_atendido_control
        vector_actual[11][4] = tiempo_permanencia_AC_control
        promedio_cal = np.round(tiempo_permanencia_AC_control / cantidad_grupos_atendido_control, decimals=3)
        vector_actual[11][5] = promedio_cal

        '''if not rnd_sorteo is None:
            
        else:
            vector_actual[6][3] = contador_sorteos
        vector_actual[12] = "Fin_Control"'''

        vector_actual[6][0] = rnd_sorteo
        vector_actual[6][1] = tiempo_sorteo
        if not tiempo_final_sorteo is None:
            vector_actual[6][2] = tiempo_final_sorteo
        vector_actual[10] = ocupado
        vector_actual[6][3] = contador_sorteos
        vector_actual[12] = "Fin_Control"

    elif evento == 6:
        rnd_premio, premio = fin_sorteo()
        vector_actual[0] = actualizar_reloj
        vector_actual[6][2] = None
        vector_actual[6][4] = rnd_premio
        vector_actual[6][5] = premio
        vector_actual[10] = libre
        vector_actual[12] = "Fin_Premio"

    elif evento == 14:
        rnd = determinar_rk()
        
        if Tipo_RK_glo == llegadas_rk:
            rk_vector_2 = RK_2(actualizar_reloj)
            tiempo_int = tiempo_RK(27, rk_vector_2)
            tiempo_final = tiempo_int + actualizar_reloj
            estado_llegadas = llegada_rota

        elif Tipo_RK_glo == servidores_rk:
            rk_vector_3 = RK_3(actualizar_reloj)
            tiempo_int = tiempo_RK(8, rk_vector_3)
            tiempo_final = tiempo_int + actualizar_reloj
            for i in range (5):
                tiempo_fin = vector_actual[5][3][i]
                if vector_actual[5][3][i] is None:
                    controles_alimentos[i].set_estado("Interrumpido")
                else:
                    controles_alimentos[i].set_interrupcion(actualizar_reloj, tiempo_fin)
                    vector_actual[5][3][i] = None

                vector_actual[9][i][0] = controles_alimentos[i].estado
               

        vector_actual[0] = actualizar_reloj
        vector_actual[14][3] = None
        vector_actual[15][0] = rnd
        vector_actual[15][1] = Tipo_RK_glo
        vector_actual[16][0] = actualizar_reloj
        vector_actual[16][1] = tiempo_int
        vector_actual[16][2] = tiempo_final
        vector_actual[12] = "Llegada RK"

    elif evento == 1 and estado_llegadas == llegada_rota:

        cola_llegadas = cola_llegadas + 1
        rnd, hora_auto, prox_auto = proximo_coche(autos, horas)
        vector_actual[0] = actualizar_reloj
        vector_actual[1][0] = rnd
        vector_actual[1][1] = hora_auto
        vector_actual[1][2] = prox_auto
        vector_actual[17] = cola_llegadas
        vector_actual[12] = "Llegada_Coche_Falla"

    elif evento == 16 and Tipo_RK_glo == llegadas_rk:

        estado_llegadas = funciona
        for i in range(cola_llegadas):
            rnd, hora_auto, prox_auto, rnd_fin, tiempo_est, fin_est, caja, promedioAC = llegada_coche(autos, horas,tiempo_est_v)

            if not prox_auto is None:
                prox_auto = np.round(prox_auto, decimals=3)
            if not fin_est is None:
                fin_est = np.round(fin_est, decimals=3)

            pos = caja.identificador
            vector_actual[0] = actualizar_reloj
            vector_actual[1][0] = rnd
            vector_actual[1][1] = hora_auto
            vector_actual[1][2] = prox_auto
            vector_actual[2][0] = rnd_fin
            vector_actual[2][1] = tiempo_est
            if not fin_est is None:
                vector_actual[2][2][pos] = fin_est
            vector_actual[7][pos][0] = ocupado
            vector_actual[7][pos][1] = caja.obtener_largo()
            if not promedioAC is None:
                vector_actual[7][pos][2] = [actualizar_reloj, promedioAC]
            vector_actual[13] = cont_llegadas
        cola_llegadas = 0
        vector_actual[17] = cola_llegadas
        vector_actual[12] = "Fin_RK_Llegadas"

        tiempo_interrup = vector_actual[14][2]
        vector_actual[14][3] = actualizar_reloj + tiempo_interrup
        vector_actual[15][0] = None
        vector_actual[15][1] = None
        vector_actual[16][0] = None
        vector_actual[16][1] = None
        vector_actual[16][2] = None

    elif evento == 16 and Tipo_RK_glo == servidores_rk:
        estado_llegadas = funciona

        for i in range(5):
            remanente = controles_alimentos[i].remanente
            if not remanente is None:
                vector_actual[5][3][i] = remanente + actualizar_reloj
            controles_alimentos[i].set_desinterrupcion()
            vector_actual[9][i][0] = controles_alimentos[i].estado
        vector_actual[0] = actualizar_reloj
        vector_actual[12] = "Fin_RK_Servidores"

        tiempo_interrup = vector_actual[14][2]
        vector_actual[14][3] = actualizar_reloj + tiempo_interrup
        vector_actual[15][0] = None
        vector_actual[15][1] = None
        vector_actual[16][0] = None
        vector_actual[16][1] = None
        vector_actual[16][2] = None
       


    #print('ESTE ES EL LARGO QUE DEVUELVE EL PASO VECTOR', len(vector_actual))
    return vector_actual, cola_caminando, rk1_vector, rk_vector_2,rk_vector_3



def llegada_coche(autos, horas,tiempo_est_v):
    global cont_llegadas
    rnd, hora_auto, prox_auto = proximo_coche(autos, horas)
    cont_llegadas = cont_llegadas + 1
    bandera, caja = Hay_Caja_Estacionamiento()
    if bandera:
        nuevo_coche = Coche(siendo_atendido, reloj)
        caja.set_estado(ocupado)
        caja.set_coche(nuevo_coche)
        rnd_fin, tiempo_est, fin_est = final_estacionamiento(tiempo_est_v)
        promedioAC = None
    else:
        caja = Buscar_Menor_Cola()
        nuevo_coche = Coche(esperando_atencion, reloj)
        promedioAC = caja.set_promedioAC(reloj)
        caja.agregar_cola(nuevo_coche)
        rnd_fin, tiempo_est, fin_est = None, None, None

    return rnd, hora_auto, prox_auto, rnd_fin, tiempo_est, fin_est, caja, promedioAC


def fin_atencion_estacionamiento(caja: Caja_Estacionamiento,tiempo_est_v):
    if caja.obtener_largo() > 0:
        promedioAC = caja.set_promedioAC(reloj)
        caja.set_tiempo(reloj)
        coche = caja.siguiente_cola()
        coche.set_estado(siendo_atendido)
        caja.set_coche(coche)
        rnd_fin, tiempo_est, fin_est = final_estacionamiento(tiempo_est_v)
        return rnd_fin, tiempo_est, fin_est, ocupado, promedioAC, reloj
    else:
        caja.set_estado(libre)
        promedioAC = None
        tiempo_cola = caja.tiempo_cola
        caja.set_coche(None)
        return None, None, None, libre, promedioAC, tiempo_cola


def final_estacionamiento(tiempo_est_v):
    tiempo_est, rnd_fin = random_fin_estacionamiento(tiempo_est_v)
    fin_est = reloj + tiempo_est
    return rnd_fin, tiempo_est, fin_est


# Genero el RND de la hora de llegada del proximo coche
def proximo_coche(autos,horas):
    tiempo_coche, rnd_coche = random_llegada_coche(autos, horas)
    llegada_proximo_coche = reloj + tiempo_coche
    return [rnd_coche, tiempo_coche, llegada_proximo_coche]


# Buscar si hay una caja libre y devolver la caja libre
def Hay_Caja_Estacionamiento():
    bandera = False
    for caja in cajas_estacionamiento:
        if caja.estado == libre:
            bandera = True
            return bandera, caja
    return bandera, None


def Buscar_Menor_Cola():
    menor_valor = float('inf')  # Valor inicial asumido como infinito
    for i in cajas_estacionamiento:
        valor = i.obtener_largo()
        if valor < menor_valor:
            menor_valor = valor
            caja = i

    return caja


# Pasaron 5 minutos desde fin estacionamiento

def llegada_del_estacionamiento(tiempo_bol_v,tiempo_con):
    entrada, rnd = random_tiene_entrada()
    if entrada:
        grupo = Grupo(None)
        rnd_control, personas_control, tiempo_control, control = llegada_control(grupo,tiempo_con)
        rnd_bol, tiempo_bol, tiempo_fin_bol, promedioAC, largo_cola_bol, caja, cola = None, None, None, None, None, None, None
    else:
        rnd_bol, tiempo_bol, tiempo_fin_bol, promedioAC, largo_cola_bol, caja, cola = llegada_boleteria(tiempo_bol_v)
        rnd_control, personas_control, tiempo_control, control = None, None, None, None

    return rnd, entrada, rnd_control, personas_control, tiempo_control, control, rnd_bol, tiempo_bol, tiempo_fin_bol, promedioAC, largo_cola_bol, caja, cola


def llegada_boleteria(tiempo_bol_v):
    bandera, caja = Hay_Caja_Boleteria()

    if bandera:
        largo_cola = 0
        cola = -1
        promedioAC = None
        grupo = Grupo(sa_boleteria)
        caja.set_estado(ocupado)
        caja.set_grupo(grupo)
        rnd, tiempo, tiempofinal = final_boleteria(tiempo_bol_v)

    else:
        grupo = Grupo(ea_boleteria)
        grupo.set_tiempo_entrada(reloj)
        caja = -1
        cola = Buscar_Menor_Cola_Boleteria()
        cola.agregar_cola(grupo)
        largo_cola = len(cola.cola)
        promedioAC = cola.set_promedioAC(reloj)
        rnd, tiempo, tiempofinal = None, None, None

    return rnd, tiempo, tiempofinal, promedioAC, largo_cola, caja, cola


# Busco si hay caja de boleteria libre y la devuelvo
def Hay_Caja_Boleteria():
    bandera = False
    for caja in cajas_boleteria:
        if caja.estado == libre:
            bandera = True
            return bandera, caja
    return bandera, None


# Busca la caja con menor cola y la devuelve
def Buscar_Menor_Cola_Boleteria():
    menor_valor = float('inf')  # Valor inicial asumido como infinito
    for i in colas_grupos:
        valor = i.obtener_largo()
        if valor < menor_valor:
            menor_valor = valor
            cola = i

    return cola


def final_boleteria(tiempo_bol_v):
    tiempo_est, rnd_fin = random_fin_boleteria(tiempo_bol_v)
    fin_est = reloj + tiempo_est
    return rnd_fin, tiempo_est, fin_est


def fin_atencion_boleteria(caja: Caja_Boleteria,tiempo_con, tiempo_bol_v):
    global tiempo_permanencia_AC_boleteria
    global cantidad_grupos_atendido_boleteria
    grupo = caja.atendiendo
    tiempo_entrada = grupo.tiempo_llegada_boleteria
    if not tiempo_entrada is None:
        tiempo_permanencia_AC_boleteria = tiempo_permanencia_AC_boleteria + (reloj - tiempo_entrada)
    cantidad_grupos_atendido_boleteria = cantidad_grupos_atendido_boleteria + 1

    if caja.cola.obtener_largo() > 0:
        caja.cola.set_promedioAC(reloj)
        promedioAC = caja.cola.promedio_grupos
        grupo_nuevo = caja.cola.siguiente_cola()
        grupo_nuevo.set_tiempo_entrada(reloj)
        caja.set_grupo(grupo_nuevo)
        rnd, tiempo, tiempo_fin = final_boleteria(tiempo_bol_v)


    else:
        promedioAC = None
        caja.set_estado(libre)
        caja.set_grupo(None)
        rnd, tiempo, tiempo_fin = None, None, None

    rnd_per, personas, tiempo_per, control = llegada_control(grupo,tiempo_con)
    estado = caja.estado
    return rnd, tiempo, tiempo_fin, promedioAC, estado, rnd_per, personas, tiempo_per, control


def llegada_control(grupo: Grupo,tiempo_con):
    bandera, control = Hay_Control_Alimento()

    if bandera:
        grupo.set_estado(sa_control)
        control.set_estado(ocupado)
        control.set_grupo(grupo)
        rnd, personas = Cantidad_Grupo()
        tiempo = personas * tiempo_con

    else:
        grupo.set_estado(ea_control)
        grupo.set_tiempo_alimento(reloj)
        control = Buscar_Menor_Cola_Alimento()
        control.agregar_cola(grupo)
        rnd, personas, tiempo = None, None, None

    return rnd, personas, tiempo, control


def Buscar_Menor_Cola_Alimento():
    menor_valor = float('inf')  # Valor inicial asumido como infinito
    for i in controles_alimentos:
        valor = len(i.cola)
        if valor < menor_valor:
            menor_valor = valor
            control = i

    return control



# Busco si hay ccontrol alimento libre y la devuelvo
def Hay_Control_Alimento():
    bandera = False
    for control in controles_alimentos:
        if control.estado == libre:
            bandera = True
            return bandera, control
    return bandera, None


def fin_control_alimentos(control: Control_Alimento,tiempo_sor):
    global tiempo_permanencia_AC_control
    global cantidad_grupos_atendido_control
    grupo = control.atendiendo
    if not grupo is None:
        if grupo.tiempo_llegada_alimentos is None:
            tiempo_entrada = None
        else:
            tiempo_entrada = grupo.tiempo_llegada_alimentos
            tiempo_permanencia_AC_control = tiempo_permanencia_AC_control + (reloj - tiempo_entrada)
    cantidad_grupos_atendido_control = cantidad_grupos_atendido_control + 1
    rnd_sorteo, tiempo_sorteo, tiempo_final_sorteo = None, None, None

    if not grupo is None:
        bandera = Toca_Sorteo()
        if bandera:
            rnd_sorteo, tiempo_sorteo, tiempo_final_sorteo = llegada_sorteo(grupo,tiempo_sor)
        else:
            rnd_sorteo, tiempo_sorteo, tiempo_final_sorteo = None,None,None

    if len(control.cola) > 0:
        grupo_nuevo = control.siguiente_cola()
        grupo_nuevo.set_estado(sa_control)
        grupo_nuevo.set_tiempo_alimento(reloj)
        control.set_grupo(grupo_nuevo)
        rnd, personas = Cantidad_Grupo()
        tiempo = personas * 5

    else:

        control.set_estado(libre)
        control.set_grupo(None)
        rnd, personas, tiempo = None, None, None
    estado = control.estado
    return rnd, personas, tiempo, estado, rnd_sorteo, tiempo_sorteo, tiempo_final_sorteo


def Toca_Sorteo():
    global contador_sorteos
    contador_sorteos = contador_sorteos + 1
    if contador_sorteos == 100:
        contador_sorteos = 0
        return True
    else:
        return False


def llegada_sorteo(grupo: Grupo,tiempo_sor):
    grupo.set_estado(sorteando)
    tiempo, rnd_sorteo = random_fin_sorteo(tiempo_sor)
    tiempo_final = tiempo + reloj 
    sorteo_0.set_grupo(grupo)
    sorteo_0.set_estado(ocupado)

    return rnd_sorteo, tiempo, tiempo_final


def fin_sorteo():
    sorteo_0.set_estado(libre)
    sorteo_0.set_grupo(None)
    rnd_premio, premio = random_premio()
    return rnd_premio, premio


def random_premio():
    rnd = np.round(random.uniform(0, 1), decimals=3)
    if rnd < 0.25:
        premio = "Remera"
    elif rnd < 0.66:
        premio = "Foto"
    else:
        premio = "Gorra"

    return rnd, premio


def random_llegada_coche(autos, horas):
    random_uniforme = np.round(random.uniform(0, 1), decimals=3)
    if random_uniforme == 1:
        random_uniforme = 0.999
    segundos = horas * 3600
    llegada_coche = generar_x_exponencial(segundos / autos, random_uniforme)
    return llegada_coche, random_uniforme


def random_fin_estacionamiento(tiempo_est_v):
    random_uniforme = np.round(random.uniform(0, 1), decimals=3)
    if random_uniforme == 1:
        random_uniforme = 0.999
    rnd_exp = generar_x_exponencial(tiempo_est_v, random_uniforme)
    return rnd_exp, random_uniforme


def random_tiene_entrada():
    random_uniforme = np.round(random.uniform(0, 1), decimals=3)

    if random_uniforme < 0.583:
        tiene_entrada = True
    else:
        tiene_entrada = False

    return tiene_entrada, random_uniforme


def random_fin_boleteria(tiempo_bol_v):
    random_uniforme = np.round(random.uniform(0, 1), decimals=3)
    if random_uniforme == 1:
        random_uniforme = 0.999
    muestra = generar_x_exponencial(tiempo_bol_v, random_uniforme)
    return muestra, random_uniforme


def random_fin_control():
    random_uniforme = np.round(random.uniform(0, 1), decimals=3)
    if random_uniforme == 1:
        random_uniforme = 0.999
    muestra = generar_x_exponencial(5, random_uniforme)
    return muestra, random_uniforme


def random_fin_sorteo(tiempo_sor):
    random_uniforme = np.round(random.uniform(0, 1), decimals=3)
    if random_uniforme == 1:
        random_uniforme = 0.999
    muestra = generar_x_exponencial(tiempo_sor, random_uniforme)
    return muestra, random_uniforme


def generar_x_exponencial(media, random_uniforme):
    rnd = (-media) * (math.log(1 - random_uniforme))
    tiempo_truncado = np.round(rnd, decimals=3)
    return tiempo_truncado


def Cantidad_Grupo():
    rnd = np.round(random.random(), decimals=3)
    if rnd > 0.833:
        personas = 4
    else:
        personas = 5
    return rnd, personas


def eliminar_coche(coche: Coche, lista_coches: List[Coche]):
    if coche in lista_coches:
        lista_coches.remove(coche)

def determinar_rk():
    global Tipo_RK_glo
    rnd = np.round(random.random(), decimals=3)
    if rnd < 0.35:
        Tipo_RK_glo = llegadas_rk
    else:
        Tipo_RK_glo = servidores_rk
    return rnd

def Crear_Objetos():
    caja_estacionamiento_0 = Caja_Estacionamiento(0)
    caja_estacionamiento_1 = Caja_Estacionamiento(1)
    caja_estacionamiento_2 = Caja_Estacionamiento(2)
    caja_estacionamiento_3 = Caja_Estacionamiento(3)
    caja_estacionamiento_4 = Caja_Estacionamiento(4)

    cola_grupo_0 = Cola_Grupos(0)
    cola_grupo_1 = Cola_Grupos(1)

    caja_boleteria_0 = Caja_Boleteria(0, cola_grupo_0)
    caja_boleteria_1 = Caja_Boleteria(1, cola_grupo_0)
    caja_boleteria_2 = Caja_Boleteria(2, cola_grupo_1)
    caja_boleteria_3 = Caja_Boleteria(3, cola_grupo_1)

    control_alimento_0 = Control_Alimento(0)
    control_alimento_1 = Control_Alimento(1)
    control_alimento_2 = Control_Alimento(2)
    control_alimento_3 = Control_Alimento(3)
    control_alimento_4 = Control_Alimento(4)

    sorteo_0 = Sorteo()

    cajas_estacionamiento = [caja_estacionamiento_0, caja_estacionamiento_1, caja_estacionamiento_2,
                             caja_estacionamiento_3, caja_estacionamiento_4]
    cajas_boleteria = [caja_boleteria_0, caja_boleteria_1, caja_boleteria_2, caja_boleteria_3]
    colas_grupos = [cola_grupo_0, cola_grupo_1]
    controles_alimentos = [control_alimento_0, control_alimento_1, control_alimento_2, control_alimento_3,
                           control_alimento_4]

    return cajas_estacionamiento, cajas_boleteria, colas_grupos, controles_alimentos, sorteo_0


cajas_estacionamiento, cajas_boleteria, colas_grupos, controles_alimentos, sorteo_0 = Crear_Objetos()

#Actualizado biennn

