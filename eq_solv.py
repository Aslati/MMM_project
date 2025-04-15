import numpy as np
import matplotlib.pyplot as plt
import control as cl
import scipy as sc
import control.matlab as cmtl
import streamlit as sl
import pandas as pd
import time

def Euler(time_axis):
    'Starting a long computation...'

    # Add a placeholder
    # latest_iteration = sl.empty()
    # bar = sl.progress(0)

    # for i in range(100):
    #     # Update the progress bar with each iteration.
    #     latest_iteration.text(f'Iteration {i+1}')
    #     bar.progress(i + 1)
    #     time.sleep(0.1)

    # '...and now we\'re done!'
    # print("Euler")
    some_data = []
    rng = np.random.default_rng()
    for i in range(3):
        some_data.append(rng.random()*5)
    chart_data = pd.DataFrame(
        some_data, time_axis
    )
    sl.line_chart(chart_data)

def Runge_Kutta():
    print("Runge-Kutta")
    return  0.01