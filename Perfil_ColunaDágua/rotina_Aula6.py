# -*- coding: utf-8 -*-
"""
"""Created on Fri Nov 20 22:18:39 2020

import pandas as pd
import matplotlib.pyplot as plt
import copy

diretorio = r"C:\Users\ximis\workspace\Matesp\atividade_6/"

file_name = "11E101660_20110922_130712.csv"

file_csv = diretorio + file_name

file_df = pd.read_csv(file_csv, header = 28, sep = ",")

lista = ['Pressure (Decibar)', 'Depth (Meter)', 'Temperature (Celsius)',
       'Conductivity (MicroSiemens per Centimeter)',
       'Specific conductance (MicroSiemens per Centimeter)',
       'Salinity (Practical Salinity Scale)',
       'Sound velocity (Meters per Second)',
       'Density (Kilograms per Cubic Meter)']

copy_df = copy.deepcopy(file_df[lista])

y_label = file_df['Depth (Meter)']

# plotagem da primeira figura 
fig , (ax1,ax2) = plt.subplots (nrows = 1, ncols =2, figsize = (8,4), dpi = 300) #cria figura com 2 eixos

ax1.plot(file_df['Temperature (Celsius)'], file_df['Depth (Meter)'],color ='red' )
ax1.invert_yaxis()
ax1.set_xlabel ('Temperature (Celsius)')
ax1.set_ylabel('Depth (Meter)')
ax1.set_title('Temperatura')
ax1.grid()

ax2.plot(file_df['Salinity (Practical Salinity Scale)'],file_df['Depth (Meter)'])
ax2.invert_yaxis()
ax2.set_xlabel ('Salinity')
ax2.set_ylabel('Depth (Meter)')
ax2.set_title('Salinidade')
ax2.grid()

fig.suptitle('Perfis CTds', fontsize = 18 , color = 'purple') 

plt.subplots_adjust (top=0.880 , bottom = 0.205 , left = 0.110 , right = 0.900, wspace = 0.200 , hspace= 0.210)




# plotagem da segunda Figura

fig , (ax3,ax4,ax5) = plt.subplots (nrows = 1, ncols =3, figsize = (15,7), dpi = 300) #cria figura com 2 eixos

ax3.plot(file_df['Temperature (Celsius)'],file_df['Salinity (Practical Salinity Scale)'],marker = '.' , linestyle = ' ', 
         color ='red',markersize = 10)
#ax3.invert_yaxis()
ax3.set_xlabel ('Temperature (Celsius)', fontsize = 9)
ax3.set_ylabel('Salinidade', fontsize = 9)
ax3.grid()


ax4.plot(file_df['Sound velocity (Meters per Second)'],file_df['Temperature (Celsius)'],marker = 'x' , linestyle = ' ', 
         color ='yellow',markersize = 9)
#ax4.invert_yaxis()
ax4.set_xlabel ('Velocidade do Som (m/s)', fontsize = 9)
ax4.set_ylabel('Temperatura (Celsius)', fontsize = 9)
ax4.grid()


ax5.plot(file_df['Salinity (Practical Salinity Scale)'],file_df['Sound velocity (Meters per Second)'],marker = 's' , linestyle = ' ', 
         color ='blue',markersize = 10)
#ax5.invert_yaxis()
ax5.set_xlabel ('Salinity', fontsize = 9)
ax5.set_ylabel('Velocidade do Som (m/s)', fontsize = 9)
ax5.grid()


fig.suptitle('Propagação do Som na coluna d água', fontsize = 18 , color = 'purple') 
plt.subplots_adjust (top=0.880 , bottom = 0.205 , left = 0.110 , right = 0.900, wspace = 0.200 , hspace= 0.210)