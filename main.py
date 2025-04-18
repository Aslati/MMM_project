import os
import numpy as np
import streamlit as sl
import pandas as pd
import zipfile
import time
from eq_solv import Euler, Runge_Kutta

sl.set_page_config(page_title="Project", page_icon="♥", layout="centered", initial_sidebar_state="auto", menu_items=None)

time_axis = [1, 2, 3] 

sidebar_frame=sl.sidebar

sidebar_frame.image('image.png')

#sl.markdown("CO<sub>2</sub>", unsafe_allow_html=True)

J1 = sidebar_frame.text_input("J1:")
J2 = sidebar_frame.text_input("J2:")
n1 = sidebar_frame.text_input("n1:")
n2 = sidebar_frame.text_input("n2:")
k = sidebar_frame.text_input("k:")
b = sidebar_frame.text_input("b:")


signal_type = sidebar_frame.selectbox("Sygnał", ['impuls', 'trójkątny', 'prostokątny', 'harmoniczny'])
#signal_len = sidebar_frame.slider("Długość symulacji:", 100, 10000)
#sidebar_frame_form = sl.sidebar.form("Własności sygnału")

x1E = [0]
x2E = [0]

x1RK = [0]
x2RK = [0]

match signal_type:
    case 'prostokątny':
        fill = sidebar_frame.select_slider("Wypełnienie [%]:", [25, 50, 75, 100])
        freq = sidebar_frame.select_slider("Częstotliwość [Hz]:", [10, 20, 30, 40, 50])
        amp = sidebar_frame.slider("Amplituda:", 1, 10)
    case 'harmoniczny':
        fill = sidebar_frame.slider("Wypełnienie:", 1, 100)
        amp = sidebar_frame.slider("Amplituda:", 1, 10)
    case 'impuls':
        amp = sidebar_frame.slider("Amplituda:", 1, 10)



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

    match signal_type: #make the signal table
        case 'prostokątny':
            #signaltable = np.array([amp, freq]).astype(np.int8)
            number_of_period_points = (1/freq)/0.01
            number_of_high_points = number_of_period_points*(fill/100)
            T = []
            for i in range(int(np.rint(4001/number_of_period_points))):
                for j in range(int(np.rint(number_of_high_points))):
                    T.append(amp)
                for j in range(int(np.rint(number_of_period_points-number_of_high_points))):
                    T.append(0)
            print(T)
        case 'impuls':
            T = [amp]
            for i in range(4001):
                T.append(0)
    
    params = [J, n, nnum[4], nnum[5], T]

    euler = Euler(params, x1E, x2E)
    rk = Runge_Kutta(params, x1RK, x2RK)

    progress_text = "Operation in progress. Please wait."
    my_bar = sl.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    time = rk[2]

    chart_data = pd.DataFrame(
        {'Θ1_E': euler[0], 'Θ2_E': euler[1], 
         'Θ1_RK': rk[0], 'Θ2_RK': rk[1]},
         index=time
    )

    signal = pd.DataFrame(
        T, index=time[:len(T)]
    )

    sl.line_chart(chart_data, y=["Θ1_E", "Θ2_E", "Θ1_RK", "Θ2_RK"],
         color=["#c72ac7", "#2ac76b", "#b72ac7", "#2ac798"])
    
    sl.line_chart(signal)

    euler_data=pd.DataFrame(
        {'Θ1(E)':euler[0], 'Θ2(E)': euler[1]}, index=time
    )
    rk_data=pd.DataFrame(
        {'Θ1(RK)':rk[0], 'Θ2(RK)': rk[1]}, index=time
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