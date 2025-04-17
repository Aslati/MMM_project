import os
import numpy as np
import matplotlib.pyplot as plt
import streamlit as sl
import pandas as pd
import control as cl
import scipy as sc
import control.matlab as cmtl
import zipfile
from eq_solv import Euler, Runge_Kutta, f

sl.set_page_config("Project")

time_axis = [1, 2, 3] 

sidebar_frame=sl.sidebar

sidebar_frame.image('image.png')

J1 = sidebar_frame.text_input("J1:")
J2 = sidebar_frame.text_input("J2:")
n1 = sidebar_frame.text_input("n1:")
n2 = sidebar_frame.text_input("n2:")
k = sidebar_frame.text_input("k:")
b = sidebar_frame.text_input("b:")
T = []

signal_type = sidebar_frame.selectbox("Sygnał", ['trójkątny', 'prostokątny', 'harmoniczny'])
#sidebar_frame_form = sl.sidebar.form("Własności sygnału")

x = [0]
y = [0]

# Runge_Kutta(x, y,)

# chart = pd.DataFrame(
#     Runge_Kutta(x,y,f)[1], Runge_Kutta(x,y,f)[0]
# )

# #sl.line_chart(chart)

match signal_type:
    case 'prostokątny':
        fill = sidebar_frame.slider("Wypełnienie:", 1, 100)
    case 'harmoniczny':
        fill = sidebar_frame.slider("Wypełnienie:", 1, 100)

T = []

euler_data=pd.DataFrame()
rk_data = pd.DataFrame()


def csv_for_download(data, name):
    file = data.to_csv().encode("utf-8")
    data.to_csv(name, index=None, sep=",", header=True, encoding='utf-8-sig')
    print("done")
    return file

if sidebar_frame.button("Symuluj"):
    params = [J1, J2, n1, n2, k, b, T]
    euler_data = Euler(time_axis)
    rk_data = Runge_Kutta(params, x, y)

    euler_csv = csv_for_download(euler_data, 'euler_data.csv')
    rk_csv = csv_for_download(rk_data, 'runge_kutter_data.csv')

    with zipfile.ZipFile('data.zip', 'w') as zf:
        zf.write('euler_data.csv')
        zf.write('runge_kutter_data.csv')

    os.remove('runge_kutter_data.csv')
    os.remove('euler_data.csv')
    with open("data.zip", "rb") as fp:
        sl.download_button(
            label = "Download CSV",
            data = fp,
            file_name="data.zip",
            mime="application/zip"
        ) 
    
    os.remove('data.zip')
