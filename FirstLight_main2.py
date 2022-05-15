# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 18:13:58 2021

@author: GONZALO DUARTE
"""
from FirstLight_model import *
from FirstLight_Data import *
from FirstLight_metodos import *
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import pylab
import time
#_______________________________Principal____________________________________
# ES LA VERSION FINAL DEL MAIN, AQUI SE PUEDE ELEGIR EL TIPO DE MODELO PARA EL CALCULO DEL CENTRO DE MASA Y RADIO DE LA GALAXIA

demo=False
galaxia_lista=True
galaxia_particular=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\z06\FL818_S036.a0.142.csv"

###############################################################################
# La seleccion de model 1 o model 2 se hace en la linea 49
# En la linea 29 debe escribirse elnombre del modelo elegido para que este figure en
# el .csv generado
###############################################################################

model='model_1_'

if (galaxia_lista or demo):
    lista_arreglo=listas(demo)
    lista1=lista_arreglo
    
    nombre2=lista_arreglo
    nombre2=nombre2.replace("\listas","")          
    nombre2=nombre2.replace(".csv","\ ") 
    #nombre2=r'C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\z10\ '#hay que dejar un espacio despues de la \
    nombre2=nombre2.replace(" ","")#aqui se elimina el espacio dejado anteriormente
    
       
    data=pd.read_csv(lista1)   
    arreglo=np.array(data)
    N7=len(data)
    arreglo4=np.zeros([N7,9])
    for j in range(0,N7,1):
        nombre1=(f'{arreglo[j,0]}') 
        nombre=nombre2+nombre1
        arreglo3=model_1 (nombre,galaxia_lista,demo)
        arreglo4[j,0]=arreglo3[0]#cmX
        arreglo4[j,1]=arreglo3[1]#cmY
        arreglo4[j,2]=arreglo3[2]#cmZ
        arreglo4[j,3]=arreglo3[3]#radio[2] masa total
        arreglo4[j,4]=arreglo3[4]#radio[0] radio 
        arreglo4[j,5]=arreglo3[5]#radio[1] radio efectivo
        arreglo4[j,6]=arreglo3[6]#SFR[0] tasa de formacion estelar 
        arreglo4[j,7]=arreglo3[7]#SFR[1] tasa de formacion estelar especifica
        arreglo4[j,8]=arreglo3[8]#SFR[2] es la masa total de estrellas menores a 30.000 años
        #print('\n---------------------------------------------\nlas coordenadas del centro de masa son:','\ncmX=',cmX,'\ncmY=',cmY,'\ncmZ=',cmZ)
        #print('\n---------------------------------------------\n*el radio de la galaxia central es',radio,'\n*el radio efectivo es',radio/2)
        #print('*la tasa de formacion estelar SFR y la SFR especifica (SFR/M) son',SFR[0],SFR[1],'respectivamente \n*la masa total dentro del radio efectivo es',SFR[2],'\n*la masa de la galaxia es',SFR[3],'\n*la masa total de estrellas menores a 30.000 años es',SFR[4])
    res=pd.DataFrame(arreglo4,columns=['cmX [kpc]','cmY [kpc]','cmZ [kpc]','masa_total [Msol]','radio [kpc]','radio_efectivo [kpc]','SFR [Msol/Gyr]','SFRe[1/Gyr]','masa_estrellas_jovenes [Msol]'])
    res2=pd.DataFrame(arreglo,columns=['galaxia'])
    resultado =pd.concat([res2,res], axis=1)
    #print(resultado)
    lista1=str(lista1)
    lista1=nombre2[-4:-1]
    print(lista1 +'.csv')
    resultado.to_csv(model+lista1+'.csv')

else:
    arreglo3=model_2(galaxia_particular,galaxia_lista,demo)
    #arreglo3: cmX,cmY,cmZ,radio[2],radio[0],radio[1],SFR[0],SFR[1],SFR[2]
    
    
    print('\n_____________________________________________\nLas coordenadas del centro de masa son:','\ncmX=',arreglo3[0],'\ncmY=',arreglo3[1],'\ncmZ=',arreglo3[2])
    print('\n_____________________________________________\nEl radio de la galaxia central es:',arreglo3[4],'kpcs','\nEl radio efectivo es:',arreglo3[5])
    print('La masa de la galaxia es',arreglo3[3])
    print('La tasa de formacion estelar SFR es:',arreglo3[6]/1000000000,'Msol/años','\nLa SFR especifica (SFR/M) es:',arreglo3[7]/1000000000,'1/años')
    