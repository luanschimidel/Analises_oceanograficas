# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:10:54 2020

@author: negri
"""


import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt
import seaborn as sns
import os 

diretorio = r"C:\Users\ximis\workspace\Matesp\atividade_7/"

mydict = dict() #dicionario vazio

'''================ ACESSO PARAMETROS OCEANOGRÁFICOS ================'''
nome_file = 'Sim_costaOcean.csv'
df = pd.read_csv(diretorio+nome_file, header=34, sep=',') 
lista = ['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND',
         'Hsig','Hmax','Avg_W_Tmp1','Avg_W_Tmp2','Avg_Sal']
dfocean = copy.deepcopy(df[lista]) # subset DataFrame 
dfocean['Avg_Sal'].values[dfocean['Avg_Sal'] < 30.0] = np.nan
dfocean.interpolate(method='linear', limit=7, inplace=True) # interpola 
# recorde das colunas
df_recorte = dfocean.loc[:,['YEAR','MONTH','DAY','HOUR','MINUTE','SECOND']]  
# indice formato timestamp (datetime)
dfocean.index = pd.to_datetime(df_recorte) 
# remover as colunas
dfocean.drop(['YEAR','MONTH','DAY','HOUR','MINUTE','SECOND'],  
              axis=1, inplace=True)
mydict['dfocean'] = dfocean.copy() # armazero no dicionario
'''================ FIM - ACESSO PARAMETROS OCEANOGRÁFICOS ================'''



'''================ ACESSO PARAMETROS METEOROLOGICOS ================'''
nome_file = 'Sim_costaMEt.csv'
df = pd.read_csv(diretorio+nome_file, header=21, sep=',')
lista = ['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND',
         'Avg_Air_Press','Avg_Air_Tmp','Avg_Hmt','Avg_Wnd_Sp',
         'Avg_Wnd_Dir_N','Avg_Sol_Rad']
dfmeteo = copy.deepcopy(df[lista]) # subset DataFrame
# verificar se há outras pendências, por exemplo, 'None'
print (dfmeteo[dfmeteo.values == 'None'])
dfmeteo['Avg_Wnd_Dir_N'].replace('None', np.nan, inplace=True)

print (dfmeteo.dtypes) # verifica os tipos dos dados  
#transforma para float
dfmeteo['Avg_Wnd_Dir_N']=dfmeteo['Avg_Wnd_Dir_N'].astype(float) 

dfmeteo.interpolate(method='linear', limit=7, inplace=True) # interpola  
# recorde das colunas
df_recorte = dfmeteo.loc[:,['YEAR','MONTH','DAY','HOUR','MINUTE','SECOND']]  
# indice formato timestamp (datetime)
dfmeteo.index = pd.to_datetime(df_recorte) 
# remover as colunas
dfmeteo.drop(['YEAR','MONTH','DAY','HOUR','MINUTE','SECOND'],  
              axis=1, inplace=True)
mydict['dfmeteo'] = dfmeteo.copy() # armazero o dataframe no dicionario
'''================ FIM - ACESSO PARAMETROS METEOROLOGICOS ================'''


# plotagem dos dataframes: dfocean e dfmeteo
for i in mydict.keys():
    df = mydict[i]
    
    if i == 'dfmeteo': 
        fig, axes = plt.subplots(6, 1, figsize=(11, 10), sharex=True) 
    else: 
        fig, axes = plt.subplots(5, 1, figsize=(11, 10), sharex=True)  
    
    parametros = df.columns  
    tit_graficos = df.columns  
    for param, titulo, ax in zip(parametros,tit_graficos,axes):
        # dados nativo
        ax.plot(df[param], marker='.', markersize=3, color='0.8', 
                linestyle='None', label='Nativo')
        # reamostragem semanal
        ax.plot(df[param].resample(rule='D').mean(), color='blue', 
                linewidth=2, label='Diário')
        ax.set_title(titulo)  
    plt.legend()
    

'''================ CONCATENAÇÃO DOS DATAS FRAMES ================'''
# OBS: como alterar a visualização dos data frames no console
pd.set_option('max_columns', None) # para mostrar todas as colunas do DataFrame
pd.set_option('max_columns', 10) # para mostrar 10 colunas
pd.reset_option('max_columns') # para voltar a posição default
# primeiro um teste, para visualizar o resultado da concatenação
dfocean_s = dfocean.iloc[0:200,0:2].resample(rule='D').mean()
dfmeteo_s = dfmeteo.iloc[0:200,0:2].resample(rule='D').mean()
# preserva as colunas e combina os indices
df = pd.concat([dfocean_s, dfmeteo_s], axis=1)
print (df)
# agora é pra valer!!!
dfocean_s = dfocean.resample(rule='D').mean()
dfmeteo_s = dfmeteo.resample(rule='D').mean()
df = pd.concat([dfocean_s, dfmeteo_s], axis=1)
print (df.head)
# plotagem do dataframe resultante da concatenação
fig, axes = plt.subplots(6, 2, figsize=(11, 10), sharex=True)
axes = np.ravel(axes) # lineariza os array com objetos eixos
parametros = df.columns
tit_graficos = df.columns
for param, titulo, ax in zip(parametros,tit_graficos,axes):
 ax.plot(df[param], color='blue', linewidth=2)
 ax.set_title(titulo)
# rotaciona o label de todos os eixos da figura
# https://stackoverflow.com/questions/10998621/rotate-axis-text-in-python-matplotlib
fig.autofmt_xdate(rotation=45)
fig.suptitle('Reamostragem Diária', fontsize=16)



# Usando o seaborn
import seaborn as sns
# plotagem do dataframe resultante da concatenação
fig, axes = plt.subplots(6, 2, figsize=(11, 10), sharex=True) 
axes = np.ravel(axes) # lineariza os array com objetos eixos
parametros = df.columns
meanprops={"marker":"o",
 "markerfacecolor":"white",
 "markeredgecolor":"black",
 "markersize":"5"} # como será o simbolo que define a media (mean)
for param, ax in zip(parametros,axes):
 sns.boxplot(data=df, x=df.index.month, showmeans=True,
 meanprops=meanprops, y=param, ax=ax)
 ax.set_ylabel(param)
 ax.set_title(param)
fig.suptitle('BoxPlot: Amostragem Mensal', fontsize=16)