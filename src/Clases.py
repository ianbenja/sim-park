from typing import List

class Coche:
    def __init__(self, estado, tiempo_llegada):
        self.estado = estado
        self.tiempo_llegada = tiempo_llegada
    def set_estado(self, nuevo_estado):
        self.estado = nuevo_estado

class Grupo:
    def __init__(self, estado):
        self.estado = estado
        self.tiempo_llegada_boleteria = None
        self.tiempo_llegada_alimentos = None

    def set_tiempo_entrada(self, tiempo_llegada_entrada):
        self.tiempo_llegada_boleteria = tiempo_llegada_entrada

    def set_tiempo_alimento(self, tiempo_llegada_alimento):
        self.tiempo_llegada_alimentos = tiempo_llegada_alimento

    def set_estado(self, nuevo_estado):
        self.estado = nuevo_estado

        


class Caja_Estacionamiento:
    def __init__(self,ide):
        self.identificador = ide
        self.estado = "Libre"
        self.atendiendo : Coche = None
        self.cola :List[Coche] = []
        self.tiempo_cola = 0
        self.promedio_coches = 0

    def set_coche(self, vehiculo : Coche):
        self.atendiendo = vehiculo

    def set_tiempo(self, tiempo_cambio):
        self.tiempo_cola = tiempo_cambio

    def set_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def set_promedioAC(self, tiempo_actual):

        promedio_nuevo = ((self.promedio_coches * tiempo_actual) + (len(self.cola) * (tiempo_actual-self.tiempo_cola)))/(tiempo_actual)
        self.promedio_coches = promedio_nuevo
        return promedio_nuevo

    def agregar_cola(self,vehiculo: Coche):
        self.cola.append(vehiculo)

    def obtener_largo(self):
        return len(self.cola)

    def siguiente_cola(self):
        if len(self.cola) > 0:
            return self.cola.pop(0)
        else:
            return None
        


class Cola_Grupos:
    def __init__(self,ide):
        self.identificador = ide
        self.cola :List[Grupo] = []
        self.tiempo_cola = 0
        self.promedio_grupos = 0
        

    def set_tiempo(self, tiempo_cambio):
        self.tiempo_cola = tiempo_cambio

    def set_promedioAC(self, tiempo_actual):

        promedio_nuevo = ((self.promedio_grupos * tiempo_actual) + (len(self.cola) * (tiempo_actual-self.tiempo_cola)))/(tiempo_actual)
        self.promedio_grupos = promedio_nuevo
    
    def agregar_cola(self, grupo: Grupo):
        self.cola.append(grupo)

    def siguiente_cola(self):
        if len(self.cola) > 0:
            return self.cola.pop(0)
        else:
            return None
        
    def obtener_largo(self):
        return len(self.cola)
    

class Caja_Boleteria:
    def __init__(self,ide, colas: Cola_Grupos):
        self.identificador = ide
        self.estado = "Libre"
        self.atendiendo :Grupo = None
        self.cola = colas


    def set_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def set_grupo(self, grupo: Grupo):
        self.atendiendo = grupo    
        
class Control_Alimento:
    def __init__(self,ide):
        self.identicador = ide
        self.estado = "Libre"
        self.atendiendo :Grupo = None
        self.cola :List[Grupo] = []
        self.remanente = None

    def set_grupo(self, grupo: Grupo):
        self.atendiendo = grupo

    def set_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def agregar_cola(self, grupo: Grupo):
        self.cola.append(grupo)

    def siguiente_cola(self):
        if len(self.cola) > 0:
            return self.cola.pop(0)
        else:
            return None
        
    def set_interrupcion(self,tiempo_actual,tiempo_fin):
        if not self.atendiendo is None:
            self.atendiendo.set_estado("Interrumpido")
            self.remanente = tiempo_fin - tiempo_actual
        self.estado = "Interrumpido"

    def set_desinterrupcion(self):
        if not self.atendiendo is None:
            self.atendiendo.set_estado("Siendo_Atendido_Control")
            if len(self.cola)>0:
                self.estado = "Ocupado"
        else:
            self.estado = "Libre"


class Sorteo:
    def __init__(self):
        self.estado = "Libre"
        self.atendiendo :Grupo = None
        self.contador = 0

    def set_contador(self,cont):
        self.contador = cont
    def set_grupo(self, grupo :Grupo):
        self.atendiendo = grupo

    def set_estado(self, nuevo_estado):
        self.estado = nuevo_estado

#Modificado bien