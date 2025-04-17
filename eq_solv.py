import numpy as np
import streamlit as sl
import pandas as pd

#params [J, n, k, b, T]

def dx2(params, n, x1, x2):
    dx2 = (params[4][n]*params[1]-params[2]*x1-params[3]*x2)/(params[0])
    return dx2

def Euler(params, x1, x2):
    
    x1E = x1
    x2E = x2

    time = [0]
    
    h = 0.05
    for n in range(1000):
        x1E.append(x1E[n]+h*x2E[n])
        x2E.append(x2E[n]+h*dx2(params, n, x1E[n], x2E[n]))
        time.append((n+1)*h)

    return x1E, x2E

def Runge_Kutta(paramsRK, x1, x2):
    
    x1RK=x1
    x2RK=x2

    time = [0]
    params=paramsRK
    h = 0.05
    for n in range(1000):
        
        k1_x1 = h*x2RK[n]
        k1_x2 = h*dx2(params, n, x1RK[n], x2RK[n])

        k2_x1 = h*(x2RK[n]+k1_x2/2)
        k2_x2 = h*dx2(params, n, x1RK[n]+k1_x1/2, x2RK[n]+k1_x2/2)

        k3_x1 = h*(x2RK[n] + k2_x2/2)
        k3_x2 = h*dx2(params, n, x1RK[n]+k2_x1/2, x2RK[n]+k2_x2/2)

        k4_x1 = h*(x2RK[n] + k3_x2/2)
        k4_x2 = h*dx2(params, n, x2RK[n]+k3_x2, x2RK[n]+k3_x2/2)
        
        ddx1 = 1/6*(k1_x1+2*k2_x1+2*k3_x1+k4_x1)
        ddx2 = 1/6*(k1_x2+2*k2_x2+2*k3_x2+k4_x2)

        x1RK.append(x1RK[n] + ddx1)
        x2RK.append(x2RK[n] + ddx2)
        
        time.append((n+1)*h)
        
    return x1RK, x2RK, time

def waiting():
    'Starting a long computation...'

   # Add a placeholder
    latest_iteration = sl.empty()
    bar = sl.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    '...and now we\'re done!'