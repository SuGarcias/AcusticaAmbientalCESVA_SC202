#SELECCIONAR FICHEROS
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px
import pandas as pd

root = tk.Tk()
root.withdraw()
##POP-UP

# Mostrar la ventana emergente
messagebox.showinfo(title="Guía de uso", message="1ª ventana: 'Fichero con la actividad'\n2ª ventana: 'Fichero con ruido sin actividad' \n3ª ventana: 'Fichero con la actividad evaluada cada segundo'")

file1_path = filedialog.askopenfilename(title="Fichero con la actividad") # Activitat
file2_path = filedialog.askopenfilename(title="Fichero con ruido sin actividad") # Soroll

print("File 1:", file1_path)
print("File 2:", file2_path)

#################################################################
#LLENAR DICCIONARIOS CON LOS CSV DE ACTIVIDAD Y SIN ACTIVIDAD


df = pd.read_csv(file1_path, sep=";", decimal=',', skiprows=13)
columns = df.columns.tolist()

actividad = {}

for column in columns:
    actividad[column] = df[column].tolist()


df = pd.read_csv(file2_path, sep=";", decimal=',', skiprows=13)
columns = df.columns.tolist()

fondo = {}

for column in columns:
    fondo[column] = df[column].tolist()

#################################################################
#CALCULOS para obtener LAeqTi
resultats ={}

LAeq = actividad['L A t'][0] #Nivel equivalente de la fase de actividad medido
LAres = fondo['L A t'][0] #Nivel equivalente del ruido de fondo
print('LAeq: ', LAeq)
print('LAres: ',LAres)

LAeqTi = 10*np.log10((10**(0.1*LAeq))-(10**(0.1*LAres))) #nivel equivalente de la fase de ruido de la actividad que estamos evaluando
print('LAeqTi: ',LAeqTi)

resultats['LA,eq,Ti'] = LAeqTi
resultats['LAres'] =  LAres 
    
#################################################################
#CALCULOS para las penalizaciones
####### Kf:

#Tercios de Octava de 20-160Hz
#L TO_20 t	L TO_25 t	L TO_31,5 t	L TO_40 t	L TO_50 t	L TO_63 t	L TO_80 t	L TO_100 t	L TO_125 t	L TO_160 t

#Nivel ponderado C y A por debajo de 160Hz

                                    #Ponderación C
Lpc20 =  actividad['L TO_20 t'][0] - 6.2
Lpc25 =  actividad['L TO_25 t'][0] - 4.4
Lpc31_5 =  actividad['L TO_31,5 t'][0] - 3
Lpc40 =  actividad['L TO_40 t'][0] - 2
Lpc50 =  actividad['L TO_50 t'][0] - 1.3
Lpc63 = actividad['L TO_63 t'][0] - 0.8
Lpc80 =  actividad['L TO_80 t'][0] - 0.5
Lpc100 =  actividad['L TO_100 t'][0] - 0.3
Lpc125 =  actividad['L TO_125 t'][0] - 0.2
Lpc160 =   actividad['L TO_160 t'][0] - 0.1

                                    #Ponderación A
Lpa20 =   actividad['L TO_20 t'][0] - 50.5
Lpa25 =   actividad['L TO_25 t'][0] - 44.7
Lpa31_5 =   actividad['L TO_31,5 t'][0] - 39.4
Lpa40 =   actividad['L TO_40 t'][0] - 34.6
Lpa50 =   actividad['L TO_50 t'][0] - 30.2
Lpa63 =   actividad['L TO_63 t'][0] - 26.2
Lpa80 =   actividad['L TO_80 t'][0] - 22.5
Lpa100 =   actividad['L TO_100 t'][0] - 19.1
Lpa125 =   actividad['L TO_125 t'][0] - 16.1
Lpa160 =   actividad['L TO_160 t'][0] - 13.4

#Nivel Ponderado para todo el RANGO de 20-160Hz:
LC_160 = 10*np.log10(10**(0.1*Lpc20)+10**(0.1*Lpc25)+10**(0.1*Lpc31_5)+10**(0.1*Lpc40)+10**(0.1*Lpc50)+10**(0.1*Lpc63)+10**(0.1*Lpc80)+10**(0.1*Lpc100)+10**(0.1*Lpc125)+10**(0.1*Lpc160)) 
LA_160 = 10*np.log10(10**(0.1*Lpa20)+10**(0.1*Lpa25)+10**(0.1*Lpa31_5)+10**(0.1*Lpa40)+10**(0.1*Lpa50)+10**(0.1*Lpa63)+10**(0.1*Lpa80)+10**(0.1*Lpa100)+10**(0.1*Lpa125)+10**(0.1*Lpa160))

print('LC_160: ', LC_160)
print('LA_160: ', LA_160)

Lf = LC_160 - LA_160 #Diferencia del nivel ponderado C y ponderado A (<160 Hz) calculado a partir de un espectro por tercios de octava

print('Lf: ', Lf)

if Lf < 20:
    Kf = 0
else:                                   #Umbral 
    Lb20 =   actividad['L TO_20 t'][0] - 78.5 
    Lb25 =   actividad['L TO_25 t'][0] - 68.7
    Lb31_5 =   actividad['L TO_31,5 t'][0] - 59.5
    Lb40 =   actividad['L TO_40 t'][0] - 51.1
    Lb50 =   actividad['L TO_50 t'][0] - 44
    Lb63 =   actividad['L TO_63 t'][0] - 37.5
    Lb80 =   actividad['L TO_80 t'][0] - 31.5
    Lb100 =   actividad['L TO_100 t'][0] - 26.5
    Lb125 =   actividad['L TO_125 t'][0] - 22.1
    Lb160 =   actividad['L TO_160 t'][0] - 17.9 
    
    # array de bandas Lb
    LBa = np.array([Lb20, Lb25, Lb31_5, Lb40, Lb50, Lb63, Lb80, Lb100, Lb125, Lb160])

    #histograma
    fig, ax = plt.subplots()
    ax.bar(np.arange(len(LBa)), LBa, width=0.8, color='b')
    ax.set_xticks(np.arange(len(LBa)))
    ax.set_xticklabels(['20', '25', '31,5', '40', '50','63', '80', '100', '125', '160'])
    ax.set_ylabel('Valor')
    ax.set_title('Bandas ruido de baja freq Lb')
    ax.set_ylim(bottom=-10)  # Establece el límite inferior en -10


    plt.show()

    #LB = nivel por encima del umbral auditivo (<160 Hz) calculado por tercios de octava 
    LB = 10*np.log10(10**(0.1*Lb20)+10**(0.1*Lb25)+10**(0.1*Lb31_5)+10**(0.1*Lb40)+10**(0.1*Lb50)+10**(0.1*Lb63)+10**(0.1*Lb80)+10**(0.1*Lb100)+10**(0.1*Lb125)+10**(0.1*Lb160))
    print('LB: ', LB)   
    if LB <25:
        Kf = 0
    elif 25 < LB < 35 : 
        Kf = 3
    else: 
        Kf = 6

print('Kf =', Kf)
resultats['Kf'] = Kf


## Kt:
# Lt des de 20Hz a 10KHz
LT = []
LT.append(0)#20Hz
claves = ['L TO_20 t','L TO_25 t', 'L TO_31,5 t', 'L TO_40 t', 'L TO_50 t', 'L TO_63 t', 'L TO_80 t', 'L TO_100 t', 'L TO_125 t', 'L TO_160 t', 'L TO_200 t', 'L TO_250 t', 'L TO_315 t', 'L TO_400 t', 'L TO_500 t', 'L TO_630 t', 'L TO_800 t', 'L TO_1k t', 'L TO_1k25 t', 'L TO_1k6 t', 'L TO_2k t', 'L TO_2k5 t', 'L TO_3k15 t', 'L TO_4k t', 'L TO_5k t', 'L TO_6k3 t', 'L TO_8k t', 'L TO_10k t']

for i in range(0,(len(claves)-2)):
    LT.append(actividad[claves[i+1]][0] - (actividad[claves[i]][0] + actividad[claves[i+2]][0])/2) #media aritmética de los tercios de octava adyacentes (Ls)

LT.append(0) #10KHz


Kt_l = []
for i in range(0,len(LT)):
    if i <= 8 :                  #20-125Hz
        if LT[i] < 8:           Kt_l.append(0) 
        elif 8 <= LT[i] <= 15:  Kt_l.append(3)
        else:                   Kt_l.append(6)
    elif  9 <= i <= 13:         #160-400Hz
        if LT[i] < 5:           Kt_l.append(0)
        elif 5 <= LT[i] <= 8:   Kt_l.append(3)
        else:                   Kt_l.append(6)
    else:                       #500-10KHz
        if LT[i] < 3:           Kt_l.append(0)
        elif 3 <= LT[i] <= 5:   Kt_l.append(3)
        else:                   Kt_l.append(6)
print(LT)

print(Kt_l)   
Kt = max(Kt_l)
print('Kt = ',Kt)
resultats['Kt'] = Kt

##Ki
#Necessitem el fitxer de la gravació de la activitat amb els valors per cada mostra de 1 s:
file3_path = filedialog.askopenfilename(title="Fichero con la actividad evaluada cada segundo") # Activitats 1s
print("File 3:", file3_path)
df = pd.read_csv(file3_path, sep=";", decimal=',', skiprows=13)

columns = df.columns.tolist()
actividad_1s = {}

for column in columns:
    actividad_1s[column] = df[column].tolist()

inside_log = 0
for key, value in actividad_1s.items():
    if 'L A 1s' == key:
        for i in range(len(actividad_1s[key])):# En principi esta posat pk no siguin 20 segons sino tot el temps de mesura
            inside_log += (10**(0.1*value[i]))

LAeqTi1s = 10*np.log10((1/len(actividad_1s['L A 1s']))*inside_log)
print(LAeqTi1s)

LAI = 0
for key, value in actividad_1s.items():
    if 'L A I' == key:
        for i in range(len(actividad_1s[key])):# En principi esta posat pk no siguin 20 segons sino tot el temps de mesura
            if value[i]> LAI: LAI = value[i]
            
print('LAI = ', LAI )
Li = LAI - LAeqTi1s

if Li < 3:          Ki = 0
elif 3>= Li <= 6:   Ki = 3
else:               Ki = 6

print('Ki = ', Ki)
resultats['Ki'] = Ki
#################################################################
#Calculo de Lari:
if (Kf + Kt + Ki)<9:
    Lari = LAeqTi + Kf + Kt + Ki
else: 
    Lari = LAeqTi + 9

print('LAr,i = ', Lari)
resultats['LAr,i'] = Lari
resultats['Tiempo de Evaluacion (s)'] =  len(actividad_1s['t'])
print('')
print('RESULTATS:')
print(resultats)
print('')


popup = tk.Toplevel(root)
#################################################################
#                       PLOTS       
# Lb ruido baja freq        
fig, ax = plt.subplots()
ax.bar(np.arange(len(LBa)), LBa, width=0.8, color='b')
ax.set_xticks(np.arange(len(LBa)))
ax.set_xticklabels(['20', '25', '31,5', '40', '50','63', '80', '100', '125', '160'])
ax.set_ylabel('Valor')
ax.set_title('Bandas ruido de baja freq Lb')
ax.set_ylim(bottom=-10)  # Establece el límite inferior en -10
#act.set_xticklabels(['8','16','31.5','63','125','250','500','1k','2k','4k','8k','16k','6,3','8','10','12,5','16','20', '25', '31,5', '40', '50','63', '80', '100', '125', '160','200','250','315','400','500','630','800','1k','1k25','1k6','2k','2k5','3k15','4k','5k','6k3','8k','10k','12k5','16k','20k'])

####################################################################
#Guardar resultados en un csv
import csv
with open("resultats.csv", mode="a", newline="") as resultats_csv:

    # Crear un objeto writer de csv
    writer = csv.writer(resultats_csv, delimiter=',')
    writer.writerow([file1_path, file2_path])
    for clave, valor in resultats.items():
        writer.writerow([clave, valor])

# Cerrar el archivo csv
resultats_csv.close()
####################################################################
# Crear un cuadro de texto para mostrar el diccionario
text = tk.Text(popup, width=50, height=10)
text.pack()

# Agregar el contenido del diccionario al cuadro de texto
for clave, valor in resultats.items():
    text.insert(tk.END, f"{clave}: {valor} \n")


button = tk.Button(popup, text="Close",width=30, height=2, bg="blue", fg="yellow" , command=quit)
button.pack()

popup.mainloop()


