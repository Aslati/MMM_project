import numpy as np
import matplotlib.pyplot as plt
import control as cl
import scipy as sc
import control.matlab as cmtl
import streamlit as sl
import pandas as pd
import time

#params [J, n, k, b, T]
def dx1(x1,x2):
    return x2

def dx2(params, n, x1, x2):
    dx2 = (params[4][n]*params[1]-params[2]*x1-params[3]*x2)/(params[0])
    return dx2

def Euler(time_axis):
    
    some_data = []
    rng = np.random.default_rng()
    for i in range(3):
        some_data.append(rng.random()*5)
    chart_data = pd.DataFrame(
        {"output": some_data}, time_axis
    )
    return chart_data

def Runge_Kutta(paramsRK, x1, x2):
    
    time = [0]

    params=paramsRK
    h = 0.05
    for n in range(1000):
        
        k1_x1 = h*x2[n]
        k1_x2 = h * dx2(params, n, x1[n], x2[n])

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
        
        time.append((n+1)*h)

    chart_data = pd.DataFrame(
        x2, index=time
    )
    sl.line_chart(chart_data)
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