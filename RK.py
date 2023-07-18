import pandas as pd
import numpy as np
import random


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


vector,b = RK_1(227.511)
#print(vector)
tiempo = tiempo_RK(30,vector)
#print("El tiempo es:",tiempo)
#print('len vector rk: ', len(vector))