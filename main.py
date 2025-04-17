import os
import numpy as np
import streamlit as sl
import pandas as pd
import zipfile
from eq_solv import Euler, Runge_Kutta

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


signal_type = sidebar_frame.selectbox("Sygnał", ['impuls', 'trójkątny', 'prostokątny', 'harmoniczny'])
#sidebar_frame_form = sl.sidebar.form("Własności sygnału")

x1E = [0]
x2E = [0]

x1RK = [0]
x2RK = [0]

match signal_type:
    case 'prostokątny':
        fill = sidebar_frame.slider("Wypełnienie:", 1, 100)
    case 'harmoniczny':
        fill = sidebar_frame.slider("Wypełnienie:", 1, 100)
    case 'impuls':
        amp = sidebar_frame.slider("Amplituda:", 1, 10)

T = [amp]
for i in range(1000):
    T.append(0)

euler_data=pd.DataFrame()
rk_data = pd.DataFrame()

def csv_for_download(data, name):
    #file = data.to_csv().encode("utf-8")
    data.to_csv(name, index=None, sep=",", header=True, encoding='utf-8-sig')

if sidebar_frame.button("Symuluj"):
    if n2.isnumeric and n1.isnumeric:
        ntable = np.array([n1, n2, J1, J2, k, b])
        nnum =ntable.astype(np.int8)
        n = nnum[1]/nnum[0]
        J = nnum[2]*np.power(n, 2)+nnum[3]
    params = [J, n, nnum[4], nnum[5], T]

    euler = Euler(params, x1E, x2E)
    rk = Runge_Kutta(params, x1RK, x2RK)

    time = rk[2]

    chart_data = pd.DataFrame(
        {'x1E': euler[0], 'x2E': euler[1], 
         'x1RK': rk[0], 'x2RK': rk[1]},
         index=time
    )
    sl.line_chart(chart_data, y=["x1E", "x2E", "x1RK", "x2RK"],
         color=["#c72ac7", "#2ac76b", "#b72ac7", "#2ac798"])

    euler_data=pd.DataFrame(
        {'x1(E)':euler[0], 'x2(E)': euler[1]}, index=time
    )
    rk_data=pd.DataFrame(
        {'x1(RK)':rk[0], 'x2(RK)': rk[1]}, index=time
    )

    csv_for_download(euler_data, 'euler_data.csv')
    csv_for_download(rk_data, 'runge_kutter_data.csv')

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