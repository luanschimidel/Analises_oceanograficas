# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 09:42:39 2020

@author: ximis
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
import seaborn as sns


diretorio = r"C:\Users\ximis\workspace\Matesp\atividade_5/"
arquivo = "SIMCOSTA_RJ-3_MET_2016-07-14_2019-09-12.csv"


dataframe = pd.read_csv (diretorio+arquivo,header = 21 , sep = "," )

lista = ['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND','Avg_Air_Press','Avg_Air_Tmp','Avg_Hmt','Avg_Wnd_Sp','Avg_Wnd_Dir_N','Avg_Sol_Rad']

df_subset = copy.deepcopy(dataframe[lista]) # copia o dataFrame a partir das colunas escolhidas

df_recorteDatas = df_subset.loc[:,['YEAR', 'MONTH', 'DAY', 'HOUR','MINUTE', 'SECOND']] #Recorte do dataframe nas colunas indicadas
                                
df_subset.index = pd.to_datetime(df_recorteDatas) # converte os valores da data para indice do dataframe


df_subset.drop(['YEAR', 'MONTH', 'DAY', 'HOUR','MINUTE', 'SECOND'],axis = 1, inplace = True)  # apaga as colunas do dataframe

# Tornando valores expurios em Nan
df_subset['Avg_Hmt'].values[df_subset['Avg_Hmt'] < 70] = np.nan
df_subset['Avg_Air_Tmp'].values[df_subset['Avg_Air_Tmp'] < 0] = np.nan


df_subset.interpolate(method = 'linear', limit = 7 , inplace = True )  # interpola intervalos de ate 7 linhas

df_subset.dropna(axis=0,inplace = True) # apaga linhas com valores nulos



# Remoção do periodo que os dados estavam inconsistentes
df_subset = df_subset.loc['2016-07-15':'2017-08-25']

#df_subset.plot() # plotando todas as variaveis no mesmo grafico
fig,axes = plt.subplots(5, 1, figsize=(11, 20), sharex=True)

fig.suptitle('Análise de parâmetros - SiMCosta RJ-3 buoy ', fontsize=16)

parametros = ['Avg_Air_Press','Avg_Air_Tmp','Avg_Hmt','Avg_Wnd_Sp','Avg_Sol_Rad']

tit_graficos = ['Pressão Atmosférica', 'Temperatura', 'Umidade Relativa' , 'Velocidade Média de Vento' , 'Radiação Solar']

y_label = ['hPa', 'Celsius (ºC)', '%' , 'm/s' , 'rad']


for ax , param , titulo , label in zip( axes , parametros, tit_graficos , y_label ):
    
    ax.plot(df_subset[param], marker = '.', markersize = 2, color = '0.8', linestyle = 'None', label = 'Nativo')
    ax.plot(df_subset[param].resample(rule='M').mean(), color='blue', linewidth=1.5, label='Mensal') # média mensal
    ax.plot(df_subset[param].resample(rule='W').mean(), color='red', linewidth=1.5, label='Diário') # média diária
    ax.grid(True)
    ax.set_title(titulo)
   
    ax.set_ylabel(label)

fig.savefig(diretorio + 'plotagem_dados.png')




fig, axes = plt.subplots(5, 1, figsize=(11, 10),sharex=True)


fig.suptitle('Variação mensal de parâmetros - SiMCosta RJ-3 buoy ', fontsize=16)
#    
for ax, param, titulo, label in zip(axes,parametros,tit_graficos, y_label):
    sns.boxplot(data = df_subset, x = df_subset.index.month, y = df_subset[param] ,showmeans = True,
               ax = ax)
#   
    ax.grid(True)
    ax.set_title(titulo)
    ax.set_ylabel(label)


#fig.savefig(diretorio + 'boxplot_dados.png')    