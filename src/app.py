from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import prueba_2


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
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
    array, i, rk1, rk2, rk3, historial = prueba_2.logica_vector(autos, horas, tiempo_est, tiempo_bol, tiempo_con, tiempo_sor)
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



if __name__ == "__main__":
    app.run_server(debug=True, port=8071)

#Actualizado 
