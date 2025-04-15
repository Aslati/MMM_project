import numpy as np
import matplotlib.pyplot as plt
import streamlit as sl
import pandas as pd
import control as cl
import scipy as sc
import control.matlab as cmtl
from eq_solv import Euler, Runge_Kutta

time_axis = [1, 2, 3] 


## sl.write(plt.plot(time_axis, some_data))
sidebar_frame=sl.sidebar
signal_type = sidebar_frame.selectbox("Sygnał", ['trójkątny', 'prostokątny', 'harmoniczny'])
#sidebar_frame_form = sl.sidebar.form("Własności sygnału")



match signal_type:
    case 'prostokątny':
        sidebar_frame.slider("Wypełnienie:", 1, 100)
        sidebar_frame.button("Symuluj")
    case 'harmoniczny':
        sidebar_frame.checkbox("Wypełnienie 100%")
        sidebar_frame.button("Symuluj", on_click=Euler(time_axis)) #to be fixed
##on_click=Euler(chart_data)        


    

