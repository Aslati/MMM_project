import numpy as np
import streamlit as sl
import pandas as pd

#params [J, n, k, b, T]

def dx2(params, n, x1, x2):
    dx2 = (params[4][n]*params[1]-params[2]*x1-params[3]*x2)/(params[0])
    return dx2

def Euler(params, x1, x2, h):

    
    for n in range(len(params[4])):
        x1.append(x1[n]+h*x2[n])
        x2.append(x2[n]+h*dx2(params, n, x1[n], x2[n]))

    return x1, x2

def Runge_Kutta(paramsRK, x1, x2, h):

    params=paramsRK
    
    for n in range(len(params[4])):
        
        k1_x1 = h*x2[n]
        k1_x2 = h*dx2(params, n, x1[n], x2[n])

        k2_x1 = h*(x2[n]+k1_x2/2)
        k2_x2 = h*dx2(params, n, x1[n]+k1_x1/2, x2[n]+k1_x2/2)

        k3_x1 = h*(x2[n] + k2_x2/2)
        k3_x2 = h*dx2(params, n, x1[n]+k2_x1/2, x2[n]+k2_x2/2)

        k4_x1 = h*(x2[n] + k3_x2/2)
        k4_x2 = h*dx2(params, n, x2[n]+k3_x2, x2[n]+k3_x2/2)
        
        ddx1 = 1/6*(k1_x1+2*k2_x1+2*k3_x1+k4_x1)
        ddx2 = 1/6*(k1_x2+2*k2_x2+2*k3_x2+k4_x2)

        x1.append(x1[n] + ddx1)
        x2.append(x2[n] + ddx2)
        
    return x1, x2