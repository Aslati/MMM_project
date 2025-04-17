import numpy as np
import matplotlib.pyplot as plt
import control as cl
import scipy as sc
import control.matlab as cmtl
import streamlit as sl
import pandas as pd
import time

#params [J1, J2, n1, n2, k, b, T]
params = []
def dx1(x1,x2): #pochodna y
    return x2

def dx2(x1,x2):
    return (params[6][0]*params[3]/params[2]-params[4]*x1-params[5]*x2)/(params[0]*np.power(params[3]/params[2], 2)+params[1])

def Euler(time_axis):
    
    some_data = []
    rng = np.random.default_rng()
    for i in range(3):
        some_data.append(rng.random()*5)
        print(some_data)
    chart_data = pd.DataFrame(
        {"output": some_data}, time_axis
    )
    sl.line_chart(chart_data)
    print(chart_data)
    return chart_data

def Runge_Kutta(paramsRK, x, y):
    params=paramsRK
    h = 0.1
    for n in range(100):
        x.append(x[n] + h)
        k1 = h*f(x[n], y[n])
        k2 = h*f(x[n]+h/2, y[n]+k1/2)
        k3 = h*f(x[n]+h/2, y[n]+k2/2)
        k4 = h*f(x[n]+h, y[n]+k3)
        
        dyn = 1/6*(k1+2*k2+2*k3+k4)
        y.append(y[n] + dyn)
        chart_data = pd.DataFrame(
            y, x
        )
    return chart_data 

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