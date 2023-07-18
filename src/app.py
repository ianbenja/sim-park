from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import sys
import random
import copy
import numpy as np
import math

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



def calcular_beta():
    rnd = np.round(random.random(), decimals=3)
    return rnd


def RK_1(a):
    rk1_vector = []
    rk_paso = []
    b = calcular_beta()
    h = 0.1
    xm = 0
    k1 = 0
    k2 = 0
    k3 = 0
    k4 = 0
    ym = a

    while ym/a < 3:
        k1 = b * ym
        xm_2 = xm + (h/2)
        ym_2 = ym + ((h/2) * k1)

        k2 = b * ym_2
        xm_3 = xm + (h / 2)
        ym_3 = ym + ((h / 2) * k2)

        k3 = b * ym_3
        xm_4 = xm + (h)
        ym_4 = ym + ((h) * k3)

        k4 = b * ym_4
        ym_final = ym+(h/6)*(k1+(2*k2)+(2*k3)+k4)
        rk_paso = [xm, ym, k1, k2, k3, k4, xm_4, ym_final, b]
        ym = ym_final
        xm = xm + h

        rk1_vector.append(rk_paso)
    return rk1_vector, b

def tiempo_RK(minutos,vector):
    #print('vector', vector)
    valor = vector[-1][6]
    tiempo = valor * (minutos*60)
    return tiempo

def RK_2(l):
    rk2_vector = []
    rk_paso = []
    h = 0.1
    xm = 0.1
    k1 = 0
    k2 = 0
    k3 = 0
    k4 = 0
    ym = l
    dif = 100

    while dif >= 1:
        k1 = -(ym/(0.8*(xm**2)))-ym
        xm_2 = xm + (h/2)
        ym_2 = ym + ((h/2) * k1)

        k2 = -(ym_2/(0.8*(xm_2**2)))-ym_2
        xm_3 = xm + (h / 2)
        ym_3 = ym + ((h / 2) * k2)

        k3 = -(ym_3/(0.8*(xm_3**2)))-ym_3
        xm_4 = xm + (h)
        ym_4 = ym + ((h) * k3)

        k4 = -(ym_4/(0.8*(xm_4**2)))-ym_4
        ym_final = ym+(h/6)*(k1+(2*k2)+(2*k3)+k4)
        rk_paso = [xm, ym, k1, k2, k3, k4, xm_4, ym_final]
        dif = np.abs(ym_final - ym)
        ym = ym_final
        xm = xm + h
        #print("la diferencia es:",dif)

        rk2_vector.append(rk_paso)
    return rk2_vector

def RK_3(s):

    rk3_vector = []
    rk_paso = []
    h = 0.1
    xm = 0
    k1 = 0
    k2 = 0
    k3 = 0
    k4 = 0
    ym = s
    dif = s*1.5

    while ym <= dif:
        k1 = 0.2 * ym + 3-xm
        xm_2 = xm + (h / 2)
        ym_2 = ym + ((h / 2) * k1)

        k2 = 0.2 * ym_2 + 3-xm_2
        xm_3 = xm + (h / 2)
        ym_3 = ym + ((h / 2) * k2)

        k3 = 0.2 * ym_3 + 3-xm_3
        xm_4 = xm + (h)
        ym_4 = ym + ((h) * k3)

        k4 = 0.2 * ym_4 + 3-xm_4
        ym_final = ym + (h / 6) * (k1 + (2 * k2) + (2 * k3) + k4)
        rk_paso = [xm, ym, k1, k2, k3, k4, xm_4, ym_final]
        ym = ym_final
        xm = xm + h
        #print("El valor de corte:", dif)

        rk3_vector.append(rk_paso)
    return rk3_vector


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.debug = True  # Habilitar el modo de depuración
server = app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "22rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow-y": "scroll"
}

CONTENT_STYLE = {
    "margin-left": "24rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

Header_component = dbc.Container(
    [
        html.H1("Trabajo Práctico N°5 - Simulación", style={'color': 'darkcyan'}),
        html.Hr()
    ])

Input_component = dbc.Container(children=[
    html.H2("Sistemas de espera en cola"),
    html.Hr(),
    html.H4("Cantidad de autos que ingresan: "),
    dcc.Input(id="input-autos", type="number", value=7200, inputMode='numeric', required=True, disabled=False),
    html.Br(),
    html.Br(),
    html.H4("Horas de simulación: "),
    dcc.Input(id="input-horas", type="number", value=3, inputMode='numeric', required=True, disabled=False),
    html.Br(),
    html.Br(),
    html.Hr(),
    html.H4("Variables del Modelo: "),
    html.H6("(En segundos)"),
    html.H5("Tiempo de atención en Estacionamiento: "),
    dcc.Input(id="input-estacionamiento", type="number", value=29, inputMode='numeric', required=True, disabled=True),
    # max=10000, min=0
    html.Br(),
    html.Br(),
    html.H5("Tiempo de atención en Boletería: "),
    dcc.Input(id="input-boleteria", type="number", value=92, inputMode='numeric', required=True, disabled=True),
    html.Br(),
    html.Br(),
    html.H5("Tiempo de atención en Control de alimentos: "),
    dcc.Input(id="input-control", type="number", value=5, inputMode='numeric', required=True, disabled=True),
    html.Br(),
    html.Br(),
    html.H5("Tiempo de atención en Sorteo: "),
    dcc.Input(id="input-sorteo", type="number", value=120, inputMode='numeric', required=True, disabled=True),
    html.Br(),
    html.Br(),
    html.Div([
        dbc.Checklist(['Editar'], id='check', switch=True)
    ]),
    html.Br(),
    html.Hr(),
])

Boton_generar_component = dbc.Row([
    dbc.Button("Generar Simulación", color="primary",
               id="btn-generar",
               className="mb-3")
        ])

Tabla_component = dcc.Loading(
    id="loading-output-table",
    children=[
        html.H2('VECTOR DE ESTADOS'),
        dash_table.DataTable(
        id='output-table',
        columns=[
            {'name': 'Evento', 'id': 'col0', 'type': 'any'},
            {'name': 'Reloj (minutos)', 'id': 'col1', 'type': 'any'},
            {'name': 'RND Llegada Auto', 'id': 'col2', 'type': 'any'},
            {'name': 'Tiempo entre Llegadas Autos', 'id': 'col3', 'type': 'any'},
            {'name': 'Próxima Llegada Auto', 'id': 'col4', 'type': 'any'},
            {'name': 'RND Fin Estacionamiento', 'id': 'col5', 'type': 'any'},
            {'name': 'Tiempo Atención Estacionamiento', 'id': 'col6', 'type': 'any'},
            {'name': 'Fin Atención Estacionamiento (1)', 'id': 'col7', 'type': 'any'},
            {'name': 'Fin Atención Estacionamiento (2)', 'id': 'col8', 'type': 'any'},
            {'name': 'Fin Atención Estacionamiento (3)', 'id': 'col9', 'type': 'any'},
            {'name': 'Fin Atención Estacionamiento (4)', 'id': 'col10', 'type': 'any'},
            {'name': 'Fin Atención Estacionamiento (5)', 'id': 'col11', 'type': 'any'},
            {'name': 'RND Entrada', 'id': 'col12', 'type': 'any'},
            {'name': 'Tiene Entrada', 'id': 'col13', 'type': 'any'},
            {'name': 'Próxima Llegada Grupo', 'id': 'col14', 'type': 'any'},
            {'name': 'Contador Grupos Caminando', 'id': 'col15', 'type': 'any'},
            {'name': 'RND Fin Boletería', 'id': 'col16', 'type': 'any'},
            {'name': 'Tiempo Atención Boletería', 'id': 'col17', 'type': 'any'},
            {'name': 'Fin Atención Boletería (1)', 'id': 'col18', 'type': 'any'},
            {'name': 'Fin Atención Boletería (2)', 'id': 'col19', 'type': 'any'},
            {'name': 'Fin Atención Boletería (3)', 'id': 'col20', 'type': 'any'},
            {'name': 'Fin Atención Boletería (4)', 'id': 'col21', 'type': 'any'},
            {'name': 'RND Personas', 'id': 'col22', 'type': 'any'},
            {'name': 'Cantidad Personas en el Grupo', 'id': 'col23', 'type': 'any'},
            {'name': 'Tiempo Control Alimentos', 'id': 'col24', 'type': 'any'},
            {'name': 'Fin Control Alimentos (1)', 'id': 'col25', 'type': 'any'},
            {'name': 'Fin Control Alimentos (2)', 'id': 'col26', 'type': 'any'},
            {'name': 'Fin Control Alimentos (3)', 'id': 'col27', 'type': 'any'},
            {'name': 'Fin Control Alimentos (4)', 'id': 'col28', 'type': 'any'},
            {'name': 'Fin Control Alimentos (5)', 'id': 'col29', 'type': 'any'},
            {'name': 'Contador Grupos Atendidos', 'id': 'col30', 'type': 'any'},
            {'name': 'RND Premio Sorteo', 'id': 'col31', 'type': 'any'},
            {'name': 'Premio', 'id': 'col32', 'type': 'any'},
            {'name': 'RND Fin Sorteo', 'id': 'col33', 'type': 'any'},
            {'name': 'Tiempo Sorteo', 'id': 'col34', 'type': 'any'},
            {'name': 'Fin Sorteo', 'id': 'col35', 'type': 'any'},
            {'name': 'Estado CE1', 'id': 'col36', 'type': 'any'},
            {'name': 'Cola CE1', 'id': 'col37', 'type': 'any'},
            {'name': 'Hora Cambio Cantidad Cola CE1', 'id': 'col38', 'type': 'any'},
            {'name': 'Promedio Autos CE1', 'id': 'col39', 'type': 'any'},
            {'name': 'Estado CE2', 'id': 'col40', 'type': 'any'},
            {'name': 'Cola CE2', 'id': 'col41', 'type': 'any'},
            {'name': 'Hora Cambio Cantidad Cola CE2', 'id': 'col42', 'type': 'any'},
            {'name': 'Promedio Autos CE2', 'id': 'col43', 'type': 'any'},
            {'name': 'Estado CE3', 'id': 'col44', 'type': 'any'},
            {'name': 'Cola CE3', 'id': 'col45', 'type': 'any'},
            {'name': 'Hora Cambio Cantidad Cola CE3', 'id': 'col46', 'type': 'any'},
            {'name': 'Promedio Autos CE3', 'id': 'col47', 'type': 'any'},
            {'name': 'Estado CE4', 'id': 'col48', 'type': 'any'},
            {'name': 'Cola CE4', 'id': 'col49', 'type': 'any'},
            {'name': 'Hora Cambio Cantidad Cola CE4', 'id': 'col50', 'type': 'any'},
            {'name': 'Promedio Autos CE4', 'id': 'col51', 'type': 'any'},
            {'name': 'Estado CE5', 'id': 'col52', 'type': 'any'},
            {'name': 'Cola CE5', 'id': 'col53', 'type': 'any'},
            {'name': 'Hora Cambio Cantidad Cola CE5', 'id': 'col54', 'type': 'any'},
            {'name': 'Promedio Autos CE5', 'id': 'col55', 'type': 'any'},
            {'name': 'Cola 1 Boletería', 'id': 'col56', 'type': 'any'},
            {'name': 'Estado CB1', 'id': 'col57', 'type': 'any'},
            {'name': 'Estado CB2', 'id': 'col58', 'type': 'any'},
            {'name': 'Hora Cambio Cantidad Cola 1', 'id': 'col59', 'type': 'any'},
            {'name': 'Promedio Personas Cola 1', 'id': 'col60', 'type': 'any'},
            {'name': 'Cola 2 Boletería', 'id': 'col61', 'type': 'any'},
            {'name': 'Estado CB3', 'id': 'col62', 'type': 'any'},
            {'name': 'Estado CB4', 'id': 'col63', 'type': 'any'},
            {'name': 'Hora Cambio Cantidad Cola 2', 'id': 'col64', 'type': 'any'},
            {'name': 'Promedio Personas Cola 2', 'id': 'col65', 'type': 'any'},
            {'name': 'Estado C1', 'id': 'col66', 'type': 'any'},
            {'name': 'Cola C1', 'id': 'col67', 'type': 'any'},
            {'name': 'Estado C2', 'id': 'col68', 'type': 'any'},
            {'name': 'Cola C2', 'id': 'col69', 'type': 'any'},
            {'name': 'Estado C3', 'id': 'col70', 'type': 'any'},
            {'name': 'Cola C3', 'id': 'col71', 'type': 'any'},
            {'name': 'Estado C4', 'id': 'col72', 'type': 'any'},
            {'name': 'Cola C4', 'id': 'col73', 'type': 'any'},
            {'name': 'Estado C5', 'id': 'col74', 'type': 'any'},
            {'name': 'Cola C5', 'id': 'col75', 'type': 'any'},
            {'name': 'Estado Sorteo', 'id': 'col76', 'type': 'any'},
            {'name': 'CONTADOR Cantidad Grupos Atendidos Boletería', 'id': 'col77', 'type': 'any'},
            {'name': 'ACUMULADOR Tiempos de Permanencia en Cola Boletería', 'id': 'col78', 'type': 'any'},
            {'name': 'PROMEDIO AC Tiempo de Espera en Boletería', 'id': 'col79', 'type': 'any'},
            {'name': 'CONTADOR Cantidad Grupos Atendidos Control Alimentos', 'id': 'col80', 'type': 'any'},
            {'name': 'ACUMULADOR Tiempos de Permanencia en Cola Control Alimentos', 'id': 'col81', 'type': 'any'},
            {'name': 'PROMEDIO AC Tiempo de Espera en Control Alimentos', 'id': 'col82', 'type': 'any'},
            {'name': 'CONTADOR Llegadas Autos', 'id': 'col83', 'type': 'any'},
            {'name': 'A (Parámetro RK1)', 'id': 'col84', 'type': 'any'},
            {'name': 'Betta (Parámetro RK1)', 'id': 'col85', 'type': 'any'},
            {'name': 'Tiempo Detención', 'id': 'col86', 'type': 'any'},
            {'name': 'Próxima Detención', 'id': 'col87', 'type': 'any'},
            {'name': 'RND Tipo Interrupción', 'id': 'col88', 'type': 'any'},
            {'name': 'Tipo Interrupción', 'id': 'col89', 'type': 'any'},
            {'name': 'S / L (Parámetro RK2/RK3)', 'id': 'col90', 'type': 'any'},
            {'name': 'Tiempo Fin Interrupción', 'id': 'col91', 'type': 'any'},
            {'name': 'Fin Interrupción', 'id': 'col92', 'type': 'any'},
            {'name': 'Cola Llegadas Autos', 'id': 'col93', 'type': 'any'}
        ],
        page_size=500,
        virtualization=True,
        fixed_rows={'headers': True},
        style_header={
            'text-align': 'center',
            'backgroundColor': '#b0c4de',
            'color': 'black',
            'whiteSpace': 'normal',
            'height': 'auto',
            'minWidth': '150px',
            'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis'
        },
        style_data={
            'backgroundColor': 'aliceblue',
            'color': 'black',
            'whiteSpace': 'normal',
            'height': 'auto',
            'minWidth': '150px',
            'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis'
        },
        style_cell={
            'border': '1px solid grey',
            'height': 'auto',
            'minWidth': '150px',
            'width': '150px',
            'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis'
        },
        style_table={
            'height': '1000px',
            'overflowY': 'auto',
            'overflowX': 'auto',
            'width': '100%',
            'minWidth': '100%',
            'maxWidth': '100%'
        }
    )],
    type="default"
)


Cuerpo_component = html.Div([
    Tabla_component
],
    id='div-tabla',
    style={"display": "none"}
    )

RK1_component = html.Div([
    dcc.Loading(
    id="loading-output-table",
    children=[
        html.H3(
            'Runge-Kutta 1: Determinación del momento de interrupción',
            style={'text-decoration': 'underline'}
        ),
        html.Br(),
        html.Div(
            dash_table.DataTable(
                id='output-RK1',
                columns=[
                    {'name': 'Xm', 'id': 'col_rk_1', 'type': 'any'},
                    {'name': 'Ym', 'id': 'col_rk_2', 'type': 'any'},
                    {'name': 'K1', 'id': 'col_rk_3', 'type': 'any'},
                    {'name': 'K2', 'id': 'col_rk_4', 'type': 'any'},
                    {'name': 'K3', 'id': 'col_rk_5', 'type': 'any'},
                    {'name': 'K4', 'id': 'col_rk_6', 'type': 'any'},
                    {'name': 'Xm+1', 'id': 'col_rk_7', 'type': 'any'},
                    {'name': 'Ym+1', 'id': 'col_rk_8', 'type': 'any'},
                    {'name': 'B', 'id': 'col_rk_9', 'type': 'any'}
                ],
                virtualization=True,
                fixed_rows={'headers': True},
                style_header={
                    'text-align': 'center',
                    'backgroundColor': '#b0c4de',
                    'color': 'black',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '110px',
                    'maxWidth': '110px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_data={
                    'backgroundColor': 'aliceblue',
                    'color': 'black',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '110px',
                    'maxWidth': '110px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_cell={
                    'border': '1px solid grey',
                    'height': 'auto',
                    'minWidth': '110px',
                    'width': '110px',
                    'maxWidth': '110px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_table={
                    'height': '400px',
                    'overflowY': 'auto',
                    'overflowX': 'auto',
                    'width': '80%',
                    'padding': '5px',
                    'margin': '0 auto'
                }
            ),
        )
    ]
)
],
    #id='div-rk1',
    #style={"display": "none"}
    )

RK2_component = html.Div([
    dcc.Loading(
    id="loading-output-table",
    children=[
        html.H3(
            'Runge-Kutta 2: Determinación del momento de recuperación (LLEGADAS)',
            style={'text-decoration': 'underline'}
        ),
        html.Br(),
        html.Div(
            dash_table.DataTable(
                id='output-RK2',
                columns=[
                    {'name': 'Xm', 'id': 'col_rk_1', 'type': 'any'},
                    {'name': 'Ym', 'id': 'col_rk_2', 'type': 'any'},
                    {'name': 'K1', 'id': 'col_rk_3', 'type': 'any'},
                    {'name': 'K2', 'id': 'col_rk_4', 'type': 'any'},
                    {'name': 'K3', 'id': 'col_rk_5', 'type': 'any'},
                    {'name': 'K4', 'id': 'col_rk_6', 'type': 'any'},
                    {'name': 'Xm+1', 'id': 'col_rk_7', 'type': 'any'},
                    {'name': 'Ym+1', 'id': 'col_rk_8', 'type': 'any'}
                ],
                virtualization=True,
                fixed_rows={'headers': True},
                style_header={
                    'text-align': 'center',
                    'backgroundColor': '#b0c4de',
                    'color': 'black',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '110px',
                    'maxWidth': '110px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_data={
                    'backgroundColor': 'aliceblue',
                    'color': 'black',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '110px',
                    'maxWidth': '110px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_cell={
                    'border': '1px solid grey',
                    'height': 'auto',
                    'minWidth': '110px',
                    'width': '110px',
                    'maxWidth': '110px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_table={
                    'height': '400px',
                    'overflowY': 'auto',
                    'overflowX': 'auto',
                    'width': '80%',
                    'padding': '5px',
                    'margin': '0 auto'
                }
            ),
        )
    ]
)
],
    #id='div-rk2',
    #style={"display": "block"}
    )

RK3_component = html.Div([
    dcc.Loading(
    id="loading-output-table",
    children=[
        html.H3(
            'Runge-Kutta 3: Determinación del momento de recuperación (SERVIDOR)',
            style={'text-decoration': 'underline'}
        ),
        html.Br(),
        html.Div(
            dash_table.DataTable(
                id='output-RK3',
                columns=[
                    {'name': 'Xm', 'id': 'col_rk_1', 'type': 'any'},
                    {'name': 'Ym', 'id': 'col_rk_2', 'type': 'any'},
                    {'name': 'K1', 'id': 'col_rk_3', 'type': 'any'},
                    {'name': 'K2', 'id': 'col_rk_4', 'type': 'any'},
                    {'name': 'K3', 'id': 'col_rk_5', 'type': 'any'},
                    {'name': 'K4', 'id': 'col_rk_6', 'type': 'any'},
                    {'name': 'Xm+1', 'id': 'col_rk_7', 'type': 'any'},
                    {'name': 'Ym+1', 'id': 'col_rk_8', 'type': 'any'}
                ],
                virtualization=True,
                fixed_rows={'headers': True},
                style_header={
                    'text-align': 'center',
                    'backgroundColor': '#b0c4de',
                    'color': 'black',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '110px',
                    'maxWidth': '110px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_data={
                    'backgroundColor': 'aliceblue',
                    'color': 'black',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '110px',
                    'maxWidth': '110px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_cell={
                    'border': '1px solid grey',
                    'height': 'auto',
                    'minWidth': '110px',
                    'width': '110px',
                    'maxWidth': '110px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_table={
                    'height': '400px',
                    'overflowY': 'auto',
                    'overflowX': 'auto',
                    'width': '80%',
                    'padding': '5px',
                    'margin': '0 auto'
                }
            ),
        )
    ]
)
],
    #id='div-rk3',
    #style={"display": "block"}
    )


RK_historial_component = html.Div([
    dcc.Loading(
    id="loading-output-table",
    children=[
        html.H3(
            'Historial de valores de los Runge-Kutta',
            style={'text-decoration': 'underline'}
        ),
        html.Br(),
        html.Div(
            dash_table.DataTable(
                id='output-historial',
                columns=[
                    {'name': 'RK Tipo', 'id': 'col_rk_1', 'type': 'any'},
                    {'name': 'Reloj (A/S/L)', 'id': 'col_rk_2', 'type': 'any'},
                    {'name': 'B (RND)', 'id': 'col_rk_3', 'type': 'any'},
                    {'name': 'Xm Final', 'id': 'col_rk_4', 'type': 'any'},
                    {'name': 'Tiempo (min)', 'id': 'col_rk_5', 'type': 'any'},
                    {'name': 'Tiempo (seg)', 'id': 'col_rk_6', 'type': 'any'}
                ],
                virtualization=True,
                fixed_rows={'headers': True},
                style_header={
                    'text-align': 'center',
                    'backgroundColor': '#b0c4de',
                    'color': 'black',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '150px',
                    'maxWidth': '150px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_data={
                    'backgroundColor': 'aliceblue',
                    'color': 'black',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '150px',
                    'maxWidth': '150px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_cell={
                    'border': '1px solid grey',
                    'height': 'auto',
                    'minWidth': '150px',
                    'width': '150px',
                    'maxWidth': '150px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_table={
                    'height': '400px',
                    'overflowY': 'auto',
                    'overflowX': 'auto',
                    'width': '80%',
                    'padding': '5px',
                    'margin': '0 auto'
                }
            ),
        )
    ]
)
],
    #id='div-hist',
    #style={"display": "none"}
    )

modal_error = dbc.Modal(
    [
        dbc.ModalHeader("Error"),
        dbc.ModalBody("Los datos ingresados son incorrectos. Por favor, verifique e intente nuevamente."),
    ],
    id="modal-error",
    centered=True,
    is_open=False,
)

sidebar = html.Div(
    [
        Input_component,
        html.Br(),
        Boton_generar_component
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div([
    Header_component,
    Cuerpo_component,
    RK1_component,
    html.Br(),
    RK2_component,
    html.Br(),
    RK3_component,
    html.Br(),
    RK_historial_component,
    modal_error
], id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([sidebar, content])

@app.callback(
    [Output("div-tabla", "style"),
    #Output("div-rk1", "style"),
    #Output("div-hist", "style"),
     ],
    Input("btn-generar", "n_clicks"))
def mostrar_table(n_clicks):
    if n_clicks == 0 or n_clicks is None:
        return {"display": "none"}, #{"display": "none"}, {"display": "none"}
    else:
        return {"display": "block"}, #{"display": "block"}, {"display": "block"}

@app.callback(
    [Output("output-table", "data"),
     Output("output-RK1", "data"),
     Output("output-RK2", "data"),
     Output("output-RK3", "data"),
     Output("output-historial", "data"),
     #Output("div-rk2", "style"),
     #Output("div-rk3", "style")
     ],
    Input("btn-generar", "n_clicks"),
    [State("input-autos", "value"),
     State("input-horas", "value"),
     State("input-estacionamiento", "value"),
     State("input-boleteria", "value"),
     State("input-control", "value"),
     State("input-sorteo", "value")])
def generar_arreglo_tabla(n_clicks, autos, horas, tiempo_est, tiempo_bol, tiempo_con, tiempo_sor):
    text = []
    #data = []
    if n_clicks is None:
        return [], [], [], [], [], #{"display": "none"}, {"display": "none"}
    elif autos is None:
        return [], [], [], [], [], #{"display": "none"}, {"display": "none"}
    elif horas is None:
        return [], [], [], [], [], #{"display": "none"}, {"display": "none"}
    else:
        #data, con, data_rk1, data_rk2, data_rk3, data_hist, band_rk2, band_rk3 = Generar_Simulacion(autos, horas, tiempo_est, tiempo_bol, tiempo_con, tiempo_sor)
        data, con, data_rk1, data_rk2, data_rk3, data_hist = Generar_Simulacion(autos, horas, tiempo_est, tiempo_bol, tiempo_con, tiempo_sor)
        dat = [{
                'col0': data[i]['Evento'],
                'col1': np.round(data[i]['Reloj (minutos)'], decimals=3) if isinstance(data[i]['Reloj (minutos)'], (int, float)) else None,
                'col2': np.round(data[i]['RND Llegada Auto'], decimals=3) if isinstance(data[i]['RND Llegada Auto'], (int, float)) else None,
                'col3': np.round(data[i]['Tiempo entre Llegadas Autos'], decimals=3) if isinstance(data[i]['Tiempo entre Llegadas Autos'], (int, float)) else None,
                'col4': np.round(data[i]['Próxima Llegada Auto'], decimals=3) if isinstance(data[i]['Próxima Llegada Auto'], (int, float)) else None,
                'col5': np.round(data[i]['RND Fin Estacionamiento'], decimals=3) if isinstance(data[i]['RND Fin Estacionamiento'], (int, float)) else None,
                'col6': np.round(data[i]['Tiempo Atención Estacionamiento'], decimals=3) if isinstance(data[i]['Tiempo Atención Estacionamiento'], (int, float)) else None,
                'col7': np.round(data[i]['Fin Atención Estacionamiento (1)'], decimals=3) if isinstance(data[i]['Fin Atención Estacionamiento (1)'], (int, float)) else None,
                'col8': np.round(data[i]['Fin Atención Estacionamiento (2)'], decimals=3) if isinstance(data[i]['Fin Atención Estacionamiento (2)'], (int, float)) else None,
                'col9': np.round(data[i]['Fin Atención Estacionamiento (3)'], decimals=3) if isinstance(data[i]['Fin Atención Estacionamiento (3)'], (int, float)) else None,
                'col10': np.round(data[i]['Fin Atención Estacionamiento (4)'], decimals=3) if isinstance(data[i]['Fin Atención Estacionamiento (4)'], (int, float)) else None,
                'col11': np.round(data[i]['Fin Atención Estacionamiento (5)'], decimals=3) if isinstance(data[i]['Fin Atención Estacionamiento (5)'], (int, float)) else None,
                'col12': np.round(data[i]['RND Entrada'], decimals=3) if isinstance(data[i]['RND Entrada'], (int, float)) else None,
                'col13': data[i]['Tiene Entrada'],
                'col14': np.round(data[i]['Próxima Llegada Grupo'], decimals=3) if isinstance(data[i]['Próxima Llegada Grupo'], (int, float)) else None,
                'col15': data[i]['Contador Grupos Caminando'],
                'col16': np.round(data[i]['RND Fin Boletería'], decimals=3) if isinstance(data[i]['RND Fin Boletería'], (int, float)) else None,
                'col17': np.round(data[i]['Tiempo Atención Boletería'], decimals=3) if isinstance(data[i]['Tiempo Atención Boletería'], (int, float)) else None,
                'col18': np.round(data[i]['Fin Atención Boletería (1)'], decimals=3) if isinstance(data[i]['Fin Atención Boletería (1)'], (int, float)) else None,
                'col19': np.round(data[i]['Fin Atención Boletería (2)'], decimals=3) if isinstance(data[i]['Fin Atención Boletería (2)'], (int, float)) else None,
                'col20': np.round(data[i]['Fin Atención Boletería (3)'], decimals=3) if isinstance(data[i]['Fin Atención Boletería (3)'], (int, float)) else None,
                'col21': np.round(data[i]['Fin Atención Boletería (4)'], decimals=3) if isinstance(data[i]['Fin Atención Boletería (4)'], (int, float)) else None,
                'col22': np.round(data[i]['RND Personas'], decimals=3) if isinstance(data[i]['RND Personas'], (int, float)) else None,
                'col23': data[i]['Cantidad Personas en el Grupo'],
                'col24': np.round(data[i]['Tiempo Control Alimentos'], decimals=3) if isinstance(data[i]['Tiempo Control Alimentos'], (int, float)) else None,
                'col25': np.round(data[i]['Fin Control Alimentos (1)'], decimals=3) if isinstance(data[i]['Fin Control Alimentos (1)'], (int, float)) else None,
                'col26': np.round(data[i]['Fin Control Alimentos (2)'], decimals=3) if isinstance(data[i]['Fin Control Alimentos (2)'], (int, float)) else None,
                'col27': np.round(data[i]['Fin Control Alimentos (3)'], decimals=3) if isinstance(data[i]['Fin Control Alimentos (3)'], (int, float)) else None,
                'col28': np.round(data[i]['Fin Control Alimentos (4)'], decimals=3) if isinstance(data[i]['Fin Control Alimentos (4)'], (int, float)) else None,
                'col29': np.round(data[i]['Fin Control Alimentos (5)'], decimals=3) if isinstance(data[i]['Fin Control Alimentos (5)'], (int, float)) else None,
                'col30': data[i]['Contador Grupos Atendidos'],
                'col31': np.round(data[i]['RND Premio Sorteo'], decimals=3) if isinstance(data[i]['RND Premio Sorteo'], (int, float)) else None,
                'col32': data[i]['Premio'],
                'col33': np.round(data[i]['RND Fin Sorteo'], decimals=3) if isinstance(data[i]['RND Fin Sorteo'], (int, float)) else None,
                'col34': np.round(data[i]['Tiempo Sorteo'], decimals=3) if isinstance(data[i]['Tiempo Sorteo'], (int, float)) else None,
                'col35': np.round(data[i]['Fin Sorteo'], decimals=3) if isinstance(data[i]['Fin Sorteo'], (int, float)) else None,
                'col36': data[i]['Estado CE1'],
                'col37': data[i]['Cola CE1'],
                'col38': np.round(data[i]['Hora Cambio Cantidad Cola CE1'], decimals=3) if isinstance(data[i]['Hora Cambio Cantidad Cola CE1'], (int, float)) else None,
                'col39': np.round(data[i]['Promedio Autos CE1'], decimals=3) if isinstance(data[i]['Promedio Autos CE1'], (int, float)) else None,
                'col40': data[i]['Estado CE2'],
                'col41': data[i]['Cola CE2'],
                'col42': np.round(data[i]['Hora Cambio Cantidad Cola CE2'], decimals=3) if isinstance(data[i]['Hora Cambio Cantidad Cola CE2'], (int, float)) else None,
                'col43': np.round(data[i]['Promedio Autos CE2'], decimals=3) if isinstance(data[i]['Promedio Autos CE2'], (int, float)) else None,
                'col44': data[i]['Estado CE3'],
                'col45': data[i]['Cola CE3'],
                'col46': np.round(data[i]['Hora Cambio Cantidad Cola CE3'], decimals=3) if isinstance(data[i]['Hora Cambio Cantidad Cola CE3'], (int, float)) else None,
                'col47': np.round(data[i]['Promedio Autos CE3'], decimals=3) if isinstance(data[i]['Promedio Autos CE3'], (int, float)) else None,
                'col48': data[i]['Estado CE4'],
                'col49': data[i]['Cola CE4'],
                'col50': np.round(data[i]['Hora Cambio Cantidad Cola CE4'], decimals=3) if isinstance(data[i]['Hora Cambio Cantidad Cola CE4'], (int, float)) else None,
                'col51': np.round(data[i]['Promedio Autos CE4'], decimals=3) if isinstance(data[i]['Promedio Autos CE4'], (int, float)) else None,
                'col52': data[i]['Estado CE5'],
                'col53': data[i]['Cola CE5'],
                'col54': np.round(data[i]['Hora Cambio Cantidad Cola CE5'], decimals=3) if isinstance(data[i]['Hora Cambio Cantidad Cola CE5'], (int, float)) else None,
                'col55': np.round(data[i]['Promedio Autos CE5'], decimals=3) if isinstance(data[i]['Promedio Autos CE5'], (int, float)) else None,
                'col56': data[i]['Cola 1 Boletería'],
                'col57': data[i]['Estado CB1'],
                'col58': data[i]['Estado CB2'],
                'col59': np.round(data[i]['Hora Cambio Cantidad Cola 1'], decimals=3) if isinstance(data[i]['Hora Cambio Cantidad Cola 1'], (int, float)) else None,
                'col60': np.round(data[i]['Promedio Personas Cola 1'], decimals=3) if isinstance(data[i]['Promedio Personas Cola 1'], (int, float)) else None,
                'col61': data[i]['Cola 2 Boletería'],
                'col62': data[i]['Estado CB3'],
                'col63': data[i]['Estado CB4'],
                'col64': np.round(data[i]['Hora Cambio Cantidad Cola 2'], decimals=3) if isinstance(data[i]['Hora Cambio Cantidad Cola 2'], (int, float)) else None,
                'col65': np.round(data[i]['Promedio Personas Cola 2'], decimals=3) if isinstance(data[i]['Promedio Personas Cola 2'], (int, float)) else None,
                'col66': data[i]['Estado C1'],
                'col67': data[i]['Cola C1'],
                'col68': data[i]['Estado C2'],
                'col69': data[i]['Cola C2'],
                'col70': data[i]['Estado C3'],
                'col71': data[i]['Cola C3'],
                'col72': data[i]['Estado C4'],
                'col73': data[i]['Cola C4'],
                'col74': data[i]['Estado C5'],
                'col75': data[i]['Cola C5'],
                'col76': data[i]['Estado Sorteo'],
                'col77': data[i]['CONTADOR Cantidad Grupos Atendidos Boletería'],
                'col78': np.round(data[i]['ACUMULADOR Tiempos de Permanencia en Cola Boletería'], decimals=3) if isinstance(data[i]['ACUMULADOR Tiempos de Permanencia en Cola Boletería'], (int, float)) else None,
                'col79': np.round(data[i]['PROMEDIO AC Tiempo de Espera en Boletería'], decimals=3) if isinstance(data[i]['PROMEDIO AC Tiempo de Espera en Boletería'], (int, float)) else None,
                'col80': data[i]['CONTADOR Cantidad Grupos Atendidos Control Alimentos'],
                'col81': np.round(data[i]['ACUMULADOR Tiempos de Permanencia en Cola Control Alimentos'], decimals=3) if isinstance(data[i]['ACUMULADOR Tiempos de Permanencia en Cola Control Alimentos'], (int, float)) else None,
                'col82': np.round(data[i]['PROMEDIO AC Tiempo de Espera en Control Alimentos'], decimals=3) if isinstance(data[i]['PROMEDIO AC Tiempo de Espera en Control Alimentos'], (int, float)) else None,
                'col83': data[i]['CONTADOR Llegadas Autos'],
                'col84': np.round(data[i]['A (Parámetro RK1)'], decimals=3) if isinstance(data[i]['A (Parámetro RK1)'], (int, float)) else None,
                'col85': np.round(data[i]['Betta (Parámetro RK1)'], decimals=3) if isinstance(data[i]['Betta (Parámetro RK1)'], (int, float)) else None,
                'col86': np.round(data[i]['Tiempo Detención'], decimals=3) if isinstance(data[i]['Tiempo Detención'], (int, float)) else None,
                'col87': np.round(data[i]['Próxima Detención'], decimals=3) if isinstance(data[i]['Próxima Detención'], (int, float)) else None,
                'col88': np.round(data[i]['RND Tipo Interrupción'], decimals=3) if isinstance(data[i]['RND Tipo Interrupción'], (int, float)) else None,
                'col89': data[i]['Tipo Interrupción'],
                'col90': np.round(data[i]['S / L (Parámetro RK2/RK3)'], decimals=3) if isinstance(data[i]['S / L (Parámetro RK2/RK3)'], (int, float)) else None,
                'col91': np.round(data[i]['Tiempo Fin Interrupción'], decimals=3) if isinstance(data[i]['Tiempo Fin Interrupción'], (int, float)) else None,
                'col92': np.round(data[i]['Fin Interrupción'], decimals=3) if isinstance(data[i]['Fin Interrupción'], (int, float)) else None,
                'col93': data[i]['Cola Llegadas Autos']
                } for i in range(con)]

        data_rk1_lleno = [{
            'col_rk_1': np.round(data_rk1[i]['Xm'], decimals=3) if 'Xm' in data_rk1[i] else None,
            'col_rk_2': np.round(data_rk1[i]['Ym'], decimals=3) if 'Ym' in data_rk1[i] else None,
            'col_rk_3': np.round(data_rk1[i]['K1'], decimals=3) if 'K1' in data_rk1[i] else None,
            'col_rk_4': np.round(data_rk1[i]['K2'], decimals=3) if 'K2' in data_rk1[i] else None,
            'col_rk_5': np.round(data_rk1[i]['K3'], decimals=3) if 'K3' in data_rk1[i] else None,
            'col_rk_6': np.round(data_rk1[i]['K4'], decimals=3) if 'K4' in data_rk1[i] else None,
            'col_rk_7': np.round(data_rk1[i]['Xm+1'], decimals=3) if 'Xm+1' in data_rk1[i] else None,
            'col_rk_8': np.round(data_rk1[i]['Ym+1'], decimals=3) if 'Ym+1' in data_rk1[i] else None,
            'col_rk_9': np.round(data_rk1[i]['B'], decimals=3) if 'B' in data_rk1[i] else None
        } for i in range(len(data_rk1))]

        data_rk2_lleno = [{
            'col_rk_1': np.round(data_rk2[i]['Xm'], decimals=3) if 'Xm' in data_rk2[i] else None,
            'col_rk_2': np.round(data_rk2[i]['Ym'], decimals=3) if 'Ym' in data_rk2[i] else None,
            'col_rk_3': np.round(data_rk2[i]['K1'], decimals=3) if 'K1' in data_rk2[i] else None,
            'col_rk_4': np.round(data_rk2[i]['K2'], decimals=3) if 'K2' in data_rk2[i] else None,
            'col_rk_5': np.round(data_rk2[i]['K3'], decimals=3) if 'K3' in data_rk2[i] else None,
            'col_rk_6': np.round(data_rk2[i]['K4'], decimals=3) if 'K4' in data_rk2[i] else None,
            'col_rk_7': np.round(data_rk2[i]['Xm+1'], decimals=3) if 'Xm+1' in data_rk2[i] else None,
            'col_rk_8': np.round(data_rk2[i]['Ym+1'], decimals=3) if 'Ym+1' in data_rk2[i] else None
        } for i in range(len(data_rk2))]

        data_rk3_lleno = [{
            'col_rk_1': np.round(data_rk3[i]['Xm'], decimals=3) if 'Xm' in data_rk3[i] else None,
            'col_rk_2': np.round(data_rk3[i]['Ym'], decimals=3) if 'Ym' in data_rk3[i] else None,
            'col_rk_3': np.round(data_rk3[i]['K1'], decimals=3) if 'K1' in data_rk3[i] else None,
            'col_rk_4': np.round(data_rk3[i]['K2'], decimals=3) if 'K2' in data_rk3[i] else None,
            'col_rk_5': np.round(data_rk3[i]['K3'], decimals=3) if 'K3' in data_rk3[i] else None,
            'col_rk_6': np.round(data_rk3[i]['K4'], decimals=3) if 'K4' in data_rk3[i] else None,
            'col_rk_7': np.round(data_rk3[i]['Xm+1'], decimals=3) if 'Xm+1' in data_rk3[i] else None,
            'col_rk_8': np.round(data_rk3[i]['Ym+1'], decimals=3) if 'Ym+1' in data_rk3[i] else None
        } for i in range(len(data_rk3))]

        data_hist_lleno = [{
            'col_rk_1': data_hist[i]['RK Tipo'],
            'col_rk_2': np.round(data_hist[i]['Reloj (A/S/L)'], decimals=3) if 'Reloj (A/S/L)' in data_hist[i] else None,
            'col_rk_3': np.round(data_hist[i]['B (RND)'], decimals=3) if 'B (RND)' in data_hist[i] else None,
            'col_rk_4': np.round(data_hist[i]['Xm Final'], decimals=3) if 'Xm Final' in data_hist[i] else None,
            'col_rk_5': np.round(data_hist[i]['Tiempo (min)'], decimals=3) if 'Tiempo (min)' in data_hist[i] else None,
            'col_rk_6': np.round(data_hist[i]['Tiempo (seg)'], decimals=3) if 'Tiempo (seg)' in data_hist[i] else None
        } for i in range(len(data_hist))]

        return dat, data_rk1_lleno, data_rk2_lleno, data_rk3_lleno, data_hist_lleno

'''
        if band_rk2 is True and band_rk3 is True:
            return dat, data_rk1_lleno, data_rk2_lleno, data_rk3_lleno, data_hist_lleno, {"display": "block"}, {"display": "block"}
        elif band_rk2 is True and band_rk3 is False:
            return dat, data_rk1_lleno, data_rk2_lleno, data_rk3_lleno, data_hist_lleno, {"display": "block"}, {"display": "none"}
        elif band_rk2 is False and band_rk3 is True:
            return dat, data_rk1_lleno, data_rk2_lleno, data_rk3_lleno, data_hist_lleno, {"display": "none"}, {"display": "block"}
        else:
            return dat, data_rk1_lleno, data_rk2_lleno, data_rk3_lleno, data_hist_lleno, {"display": "none"}, {"display": "none"}
'''

@app.callback(
    [Output("input-autos", "disabled"),
     Output("input-horas", "disabled"),
     Output("input-estacionamiento", "disabled"),
     Output("input-boleteria", "disabled"),
     Output("input-control", "disabled"),
     Output("input-sorteo", "disabled"),
     Output("input-autos", "value"),
     Output("input-horas", "value"),
     Output("input-estacionamiento", "value"),
     Output("input-boleteria", "value"),
     Output("input-control", "value"),
     Output("input-sorteo", "value")],
    [Input('check', 'value')],
    [State("input-autos", "value"),
     State("input-horas", "value"),
     State("input-estacionamiento", "value"),
     State("input-boleteria", "value"),
     State("input-control", "value"),
     State("input-sorteo", "value")]
)
def toggle_inputs(value, autos, horas, tiempo_est, tiempo_bol, tiempo_con, tiempo_sor):
    if value:
        return False, False, False, False, False, False, autos, horas, tiempo_est, tiempo_bol, tiempo_con, tiempo_sor
    else:
        return True, True, True, True, True, True, 7200, 3, 29, 92, 5, 120


@app.callback(
    Output("modal-error", "is_open"),
    [Input("btn-generar", "n_clicks")],
    [State("input-autos", "value"),
     State("input-horas", "value"),
     State("input-estacionamiento", "value"),
     State("input-boleteria", "value"),
     State("input-control", "value"),
     State("input-sorteo", "value")]
)
def mostrar_modal_error(n_clicks, autos, horas, tiempo_est, tiempo_bol, tiempo_con, tiempo_sor):
    if n_clicks is None:
        return False
    elif autos is None or horas is None or tiempo_est is None or tiempo_bol is None or tiempo_con is None or tiempo_sor is None:
        return True
    elif autos < 1 or horas < 1 or tiempo_est < 0 or tiempo_bol < 0 or tiempo_con < 0 or tiempo_sor < 0:
        return True
    else:
        return False


def Generar_Simulacion(autos, horas, tiempo_est, tiempo_bol, tiempo_con, tiempo_sor):
    array, i, rk1, rk2, rk3, historial = logica_vector(autos, horas, tiempo_est, tiempo_bol, tiempo_con, tiempo_sor)
    #print('VECTOR RK',rk1)
    #band_rk2 = None
    #band_rk3 = None
    #if not rk2 is None:
        #band_rk2 = True
    #    print('VECTOR RK2',rk2)
    #else:
        #band_rk2 = False

    #if not rk3 is None:
        #band_rk3 = True
    #    print('VECTOR RK3', rk3)
    #else:
        #band_rk3 = False

    #print('historial', historial)
    df1 = pd.DataFrame(array, columns=['Reloj (minutos)',  # [0]
                                       'RND Llegada Auto',  # [1][0]
                                       'Tiempo entre Llegadas Autos',  # [1][1]
                                       'Próxima Llegada Auto',  # [1][2]
                                       'RND Fin Estacionamiento',  # [2][0]
                                       'Tiempo Atención Estacionamiento',  # [2][1]
                                       'Fin Atención Estacionamiento (1)',  # [2][2][0]
                                       'Fin Atención Estacionamiento (2)',  # [2][2][1]
                                       'Fin Atención Estacionamiento (3)',  # [2][2][2]
                                       'Fin Atención Estacionamiento (4)',  # [2][2][3]
                                       'Fin Atención Estacionamiento (5)',  # [2][2][4]
                                       'RND Entrada',  # [3][0]
                                       'Tiene Entrada',  # [3][1]
                                       'Próxima Llegada Grupo',  # [3][2]
                                       'Contador Grupos Caminando',  # [3][3]
                                       'RND Fin Boletería',  # [4][0]
                                       'Tiempo Atención Boletería',  # [4][1]
                                       'Fin Atención Boletería (1)',  # [4][2][0]
                                       'Fin Atención Boletería (2)',  # [4][2][1]
                                       'Fin Atención Boletería (3)',  # [4][2][2]
                                       'Fin Atención Boletería (4)',  # [4][2][3]
                                       'RND Personas',  # [5][0]
                                       'Cantidad Personas en el Grupo',  # [5][1]
                                       'Tiempo Control Alimentos',  # [5][2][0]
                                       'Fin Control Alimentos (1)',  # [5][3][0]
                                       'Fin Control Alimentos (2)',  # [5][3][1]
                                       'Fin Control Alimentos (3)',  # [5][3][2]
                                       'Fin Control Alimentos (4)',  # [5][3][3]
                                       'Fin Control Alimentos (5)',  # [5][3][4]
                                       'RND Fin Sorteo',  # [6][0]
                                       'Tiempo Sorteo',  # [6][1]
                                       'Fin Sorteo',  # [6][2]
                                       'Contador Grupos Atendidos',  # [6][3]
                                       'RND Premio Sorteo',  # [6][4]
                                       'Premio',  # [6][5]
                                       'Estado CE1',  # [7][0][0]
                                       'Cola CE1',  # [7][0][1]
                                       'Promedio Autos CE1',  # [7][0][2][0]
                                       'Hora Cambio Cantidad Cola CE1',  # [7][0][2][1]
                                       'Estado CE2',  # [7][1][0]
                                       'Cola CE2',  # [7][1][1]
                                       'Promedio Autos CE2',  # [7][1][2][0]
                                       'Hora Cambio Cantidad Cola CE2',  # [7][1][2][1]
                                       'Estado CE3',  # [7][2][0]
                                       'Cola CE3',  # [7][2][1]
                                       'Promedio Autos CE3',  # [7][2][2][0]
                                       'Hora Cambio Cantidad Cola CE3',  # [7][2][2][1]
                                       'Estado CE4',  # [7][3][0]
                                       'Cola CE4',  # [7][3][1]
                                       'Promedio Autos CE4',  # [7][3][2][0]
                                       'Hora Cambio Cantidad Cola CE4',  # [7][3][2][1]
                                       'Estado CE5',  # [7][4][0]
                                       'Cola CE5',  # [7][4][1]
                                       'Promedio Autos CE5',  # [7][4][2][0]
                                       'Hora Cambio Cantidad Cola CE5',  # [7][4][2][1]
                                       'Estado CB1',  # [8][0][0][0]
                                       'Estado CB2',  # [8][0][0][1]
                                       'Cola 1 Boletería',  # [8][0][1]
                                       'Promedio Personas Cola 1',  # [8][0][2][0]
                                       'Hora Cambio Cantidad Cola 1',  # [8][0][2][1]
                                       'Estado CB3',  # [8][1][0][0]
                                       'Estado CB4',  # [8][1][0][1]
                                       'Cola 2 Boletería',  # [8][1][1]
                                       'Promedio Personas Cola 2',  # [8][1][2][0]
                                       'Hora Cambio Cantidad Cola 2',  # [8][1][2][1]
                                       'Estado C1',  # [9][0][0]
                                       'Cola C1',  # [9][0][1]
                                       'Estado C2',  # [9][1][0]
                                       'Cola C2',  # [9][1][1]
                                       'Estado C3',  # [9][2][0]
                                       'Cola C3',  # [9][2][1]
                                       'Estado C4',  # [9][3][0]
                                       'Cola C4',  # [9][3][1]
                                       'Estado C5',  # [9][4][0]
                                       'Cola C5',  # [9][4][1]
                                       'Estado Sorteo',  # [10]
                                       'CONTADOR Cantidad Grupos Atendidos Boletería',  # [11][0]
                                       'ACUMULADOR Tiempos de Permanencia en Cola Boletería',  # [11][1]
                                       'PROMEDIO AC Tiempo de Espera en Boletería',  # [11][2]
                                       'CONTADOR Cantidad Grupos Atendidos Control Alimentos',  # [11][3]
                                       'ACUMULADOR Tiempos de Permanencia en Cola Control Alimentos',  # [11][4]
                                       'PROMEDIO AC Tiempo de Espera en Control Alimentos',  # [11][5]
                                       'Evento',  # [12]
                                       'CONTADOR Llegadas Autos',
                                       'A (Parámetro RK1)',
                                       'Betta (Parámetro RK1)',
                                       'Tiempo Detención',
                                       'Próxima Detención',
                                       'RND Tipo Interrupción',
                                       'Tipo Interrupción',
                                       'S / L (Parámetro RK2/RK3)',
                                       'Tiempo Fin Interrupción',
                                       'Fin Interrupción',
                                       'Cola Llegadas Autos'
                                       ])

    df2 = pd.DataFrame(rk1, columns=[
        'Xm',
        'Ym',
        'K1',
        'K2',
        'K3',
        'K4',
        'Xm+1',
        'Ym+1',
        'B',
    ])

    df3 = pd.DataFrame(rk2, columns=[
        'Xm',
        'Ym',
        'K1',
        'K2',
        'K3',
        'K4',
        'Xm+1',
        'Ym+1',
    ])

    df4 = pd.DataFrame(rk3, columns=[
        'Xm',
        'Ym',
        'K1',
        'K2',
        'K3',
        'K4',
        'Xm+1',
        'Ym+1',
    ])

    df5 = pd.DataFrame(historial, columns=[
        'RK Tipo',
        'Reloj (A/S/L)',
        'B (RND)',
        'Xm Final',
        'Tiempo (min)',
        'Tiempo (seg)',
    ])

    data_dict1 = df1.to_dict('records')
    data_dict2 = df2.to_dict('records')
    data_dict3 = df3.to_dict('records')
    data_dict4 = df4.to_dict('records')
    data_dict5 = df5.to_dict('records')

    return data_dict1, i, data_dict2, data_dict3, data_dict4, data_dict5, #band_rk2, band_rk3


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


if __name__ == "__main__":
    app.run_server(debug=True,port=8071)

#Actualizado 
