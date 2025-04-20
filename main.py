import os
import numpy as np
import streamlit as sl
import pandas as pd
import zipfile
import time
import matplotlib.pyplot as plt
from eq_solv import Euler, Runge_Kutta

sl.set_page_config(page_title="Project", page_icon="♥", layout="centered", initial_sidebar_state="auto", menu_items=None)

sidebar_frame=sl.sidebar

sidebar_frame.image('image.png')

J1 = sidebar_frame.number_input("J1:", min_value=0.5, value=1.0, step=0.5)
J2 = sidebar_frame.number_input("J2:", min_value=0.5, value=1.0, step=0.5)
n1 = sidebar_frame.number_input("n1:", min_value=0.5, value=1.0, step=0.5)
n2 = sidebar_frame.number_input("n2:", min_value=0.5, value=1.0, step=0.5)
k = sidebar_frame.number_input("k:", min_value=0.5, value=1.0, step=0.5)
b = sidebar_frame.number_input("b:", min_value=0.5, value=1.0, step=0.5)

signal_type = sidebar_frame.selectbox("Sygnał", ['impuls', 'trójkątny', 'prostokątny', 'harmoniczny', 'skok'])

x1E = [0]
x2E = [0]

x1RK = [0]
x2RK = [0]

match signal_type:
    case 'prostokątny':
        fill = sidebar_frame.select_slider("Wypełnienie [%]:", [25, 50, 75])
        freq = sidebar_frame.select_slider("Częstotliwość [Hz]:", [1, 5, 10, 25, 50])
        amp = sidebar_frame.slider("Amplituda:", 1, 10)
        offset = sidebar_frame.slider("Offset:", -10, 10)
    case 'trójkątny':
        freq = sidebar_frame.select_slider("Częstotliwość [Hz]:", [1, 5, 25, 40, 50])
        amp = sidebar_frame.slider("Amplituda:", 1, 10)
        offset = sidebar_frame.slider("Offset:", -10, 10)
    case 'harmoniczny':
        freq = sidebar_frame.select_slider("Częstotliwość [Hz]:", [1, 5, 25, 40, 50])
        amp = sidebar_frame.slider("Amplituda:", 1, 10)
        offset = sidebar_frame.slider("Offset:", -10, 10)
    case 'impuls':
        amp = sidebar_frame.slider("Amplituda:", 1, 10)
    case 'skok':
        amp = sidebar_frame.slider("Amplituda:", 1, 10)

euler_data=pd.DataFrame()
rk_data = pd.DataFrame()

def csv_for_download(data, name):
    data.to_csv(name, index=None, sep=",", header=True, encoding='utf-8-sig')

if sidebar_frame.button("Symuluj"):

    n = n2/n1
    J = J1*np.power(n, 2)+J2
    params = [J, n, k, b]
    proceed = True

    match signal_type: #make the signal table
        case 'prostokątny':
                number_of_period_points = (1/freq)/0.01
                number_of_high_points = number_of_period_points*(fill/100)
                T = []
                for i in range(int(4001/number_of_period_points)):
                    for j in range(int(number_of_high_points)):
                        T.append(amp+offset)
                    for j in range(int(number_of_period_points-number_of_high_points)):
                        T.append(0+offset)
        case 'harmoniczny':
                number_of_period_points = int((1/freq)/0.01)
                particles = 2*np.pi/number_of_period_points
                T = []
                for i in range(int(4001/number_of_period_points)):
                    for j in range(number_of_period_points):
                        T.append(np.sin(j*particles)+offset)
        case 'trójkątny':
                number_of_period_points = (1/freq)/0.01
                number_of_one_side_points = int(number_of_period_points/4)
                T = [0+offset]
                for j in range (number_of_one_side_points):
                    T.append(T[j]+np.abs((amp+offset)/number_of_one_side_points))
                for j in range (2*number_of_one_side_points):
                    T.append(T[number_of_one_side_points+j]-np.abs((amp+offset)/number_of_one_side_points))
                for j in range (number_of_one_side_points-1):
                    T.append(T[j+3*number_of_one_side_points]+np.abs((amp+offset)/number_of_one_side_points))
                T_part = T
                for i in range(int(4000/number_of_period_points)):
                    T = np.concatenate((T, T_part), axis=None)
        case 'impuls':
                T = [amp]
                for i in range(4000):
                    T.append(0)
        case 'skok':
                T = []
                for i in range(4001):
                    T.append(amp)
        
    params.append(T) #add the signal to the parameter list

    timeT = [0]
    
    h = 0.01
    for n in range(len(T)):
        timeT.append((n+1)*h)

    euler = Euler(params, x1E, x2E, h)
    rk = Runge_Kutta(params, x1RK, x2RK, h)

    # progress_text = "Operation in progress. Please wait." #pure aesthetics
    # my_bar = sl.progress(0, text=progress_text)

    # for percent_complete in range(100):
        #     time.sleep(0.01)
        #     my_bar.progress(percent_complete + 1, text=progress_text)
    # time.sleep(1)
    # my_bar.empty()

    chart_data = pd.DataFrame(
        {'Θ1_E': euler[0], 'Θ2_E': euler[1], 
        'Θ1_RK': rk[0], 'Θ2_RK': rk[1]},
        index=timeT
    )

    signal = pd.DataFrame(
        T[:200], index=timeT[:200]
    )

    sl.line_chart(chart_data, y=["Θ1_E", "Θ2_E", "Θ1_RK", "Θ2_RK"])
        
    sl.line_chart(signal)

    euler_data=pd.DataFrame(
        {'Θ1(E)':euler[0], 'Θ2(E)': euler[1]}, index=timeT
    )
    rk_data=pd.DataFrame(
        {'Θ1(RK)':rk[0], 'Θ2(RK)': rk[1]}, index=timeT
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