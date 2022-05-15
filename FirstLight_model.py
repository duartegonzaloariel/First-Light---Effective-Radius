# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 21:33:23 2021

@author: GONZALO DUARTE
"""

from FirstLight_Data import *
from FirstLight_metodos import *
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import pylab
import time



#_________________model 1_______________________________________
# HACE EL CALCULO DEL CENTRO DE MASA Y CALCULA EL RADIO EN FUNCION DE LOS PERFILES DE MASA

def model_1(nombre,galaxia_lista,demo):
    
    #nombre=(f'{arreglo[j,0]}')
    
    print('__________________________________________________\n',nombre)
    #data=pd.read_csv(f'{nombre}')#Es el archivo generado en "read_stars_v2mod"desde el correspondiente archivo binario
    data=pd.read_csv(nombre)
    data=data.loc[:,['ID','POS_X','POS_Y','POS_Z','VEL_X','VEL_Y','VEL_Z','INIT_MASS','AGE','X_SNII','X_SNIa1','MASS_PARTICLE']]
    
    tamaño=int(nombre[-13:-11]) 
    
    
    factor=0.4
    tamaño=int(tamaño)
    MaX=tamaño
    MiX=-tamaño
    MaY=tamaño
    MiY=-tamaño
    MaZ=tamaño
    MiZ=-tamaño
    print('su caja inicial tiene de lado:',tamaño*2)
    data = data[(data['POS_X']<=MaX)& (data['POS_X']>=MiX)&(data['POS_Y']<=MaY)& (data['POS_Y']>=MiY)&(data['POS_Z']<=MaZ)& (data['POS_Z']>=MiZ)]
    
    caja=lista_masas(data,tamaño)
    MaX=caja[0]
    MiX=caja[1]
    MaY=caja[2]
    MiY=caja[3]
    MaZ=caja[4]
    MiZ=caja[5]
    R=(MaX-MiX)
    Nit=5
    R2=0
    for i in range(0,Nit,1):
        cm=CM(MaX,MiX,MaY,MiY,MaZ,MiZ,data,R)
        cmX=cm[0]
        cmY=cm[1]
        cmZ=cm[2]
        
        arreglo_rmt=distribucion(cmX,cmY,cmZ,data,tamaño)
        
        #el arregloE_M = arreglo3, es una matriz de 30*2. Cada fila representa la cantidad de estrellas en su intervalo de ancho dr
        DF=pd.DataFrame(arreglo_rmt,columns=['r','masa_acumulada','masa_dr','estrella_dr'])
        radio=cambia_pendiente(DF,factor,R2)#devuelve(radio de galaxia,radio_ef,masa)
        R=(radio[0])
        if i==0:
            R2=R
    
    
    nombre=str(nombre)
    nombre=nombre[-21:]
    
    plt.figure(1)
    DF.plot(x = 'r', y = 'masa_acumulada', kind = 'scatter' )
    plt.ylabel('masa_acumulada [Msol]')
    plt.xlabel('r [Kpc]')
    plt.title(nombre)
    plt.plot(radio[0],radio[2],marker='o',color='r') 
    dataRcm=data[(((data['POS_X']-cmX)*(data['POS_X']-cmX)+(data['POS_Y']-cmY)*(data['POS_Y']-cmY)+(data['POS_Z']-cmZ)*(data['POS_Z']-cmZ))<radio[0]*radio[0])]
    SFR=tasa_estelar(dataRcm,radio[2])#devuelve (SFR,SFRe,masa de estrellas jovenes)
    
    if (galaxia_lista==False and demo==False):
       
        dataRcm=dataRcm.loc[:,['ID','POS_X','POS_Y','POS_Z','MASS_PARTICLE']]
        dataRcm2=data[(((data['POS_X']-cmX)*(data['POS_X']-cmX)+(data['POS_Y']-cmY)*(data['POS_Y']-cmY)+(data['POS_Z']-cmZ)*(data['POS_Z']-cmZ))<25*radio[0]*radio[0])]
        N=len(DF)
        log_radio=np.zeros([N,1])
        log_masa=np.zeros([N,1])
        cont=0
        for i in range(0,N,1):
            if arreglo_rmt[i,1]!=0:
                log_radio[i]=math.log10(arreglo_rmt[i,0])
                log_masa[i]=math.log10(arreglo_rmt[i,1])
            else:
                cont=cont+1
        N2=N-cont
        log_radio2=np.zeros([N2,1])
        log_masa2=np.zeros([N2,1])
        
        for i in range(0,N2,1):
            log_radio2[i]=log_radio[i+cont]
            log_masa2[i]=log_masa[i+cont]
        plt.figure(1)
        plt.scatter(log_masa2,log_radio2,marker='.',color='k',alpha=1)
        plt.title(nombre)
        plt.xlabel('log masa [log Msol]')
        plt.ylabel('log radio [Kpc]')
        plt.plot(math.log10(radio[2]),math.log10(radio[0]),marker='o',color='r')
        
        
        DF.plot(x = 'r', y = 'masa_acumulada', kind = 'scatter' )
        plt.ylabel('masa_acumulada [Msol]')
        plt.xlabel('r [Kpc]')
        plt.title(nombre)
        plt.plot(radio[0],radio[2],marker='o',color='r')
        plt.plot(radio[1],radio[2]/2,marker='o',color='k')
        
        dataRcm2.plot( x='POS_X',y='POS_Y',kind='scatter',marker='.', alpha=0.1)
        plt.plot(cmX,cmY,marker='o',color='r')
        plt.title(nombre)
        plt.ylabel('Y [Kpc]')
        plt.xlabel('X [Kpc]')
        plt.plot(cmX+radio[0],cmY,marker='.',color='r',alpha=1)
        plt.plot(cmX-radio[0],cmY,marker='.',color='r',alpha=1)
        plt.plot(cmX,cmY+radio[0],marker='.',color='r',alpha=1)
        plt.plot(cmX,cmY-radio[0],marker='.',color='r',alpha=1)
        
        dataRcm2.plot( x='POS_X',y='POS_Z',kind='scatter',marker='.',color='g', alpha=0.1)
        plt.plot(cmX,cmZ,marker='o',color='r')
        plt.title(nombre)
        plt.ylabel('Z [Kpc]')
        plt.xlabel('X [Kpc]')
        plt.plot(cmX+radio[0],cmZ,marker='.',color='r',alpha=1)
        plt.plot(cmX-radio[0],cmZ,marker='.',color='r',alpha=1)
        plt.plot(cmX,cmZ+radio[0],marker='.',color='r',alpha=1)
        plt.plot(cmX,cmZ-radio[0],marker='.',color='r',alpha=1)
        
        dataRcm2.plot( x='POS_Y',y='POS_Z',kind='scatter',marker='.',color='k', alpha=0.1)
        plt.plot(cmY,cmZ,marker='o',color='r')
        plt.plot(cmY+radio[0],cmZ,marker='.',color='r',alpha=1)
        plt.plot(cmY-radio[0],cmZ,marker='.',color='r',alpha=1)
        plt.plot(cmY,cmZ+radio[0],marker='.',color='r',alpha=1)
        plt.plot(cmY,cmZ-radio[0],marker='.',color='r',alpha=1)
        plt.title(nombre)
        plt.ylabel('Z [Kpc]')
        plt.xlabel('Y [Kpc]')
    return(cmX,cmY,cmZ,radio[2],radio[0],radio[1],SFR[0],SFR[1],SFR[2])  



#_________________model 2_______________________________________
# TOMA COMO CENTRO X=0 Y=0 Z=0, Y DE RADIO EL RADIO DEL VIRIAL, ES DECIR 1/4 DEL LA INFORMACION CORRESPONDIENTE DEL NOMBRE DE LA GALAXIA 

def model_2(nombre,galaxia_lista,demo):
    
    #nombre=(f'{arreglo[j,0]}')
    
    print('__________________________________________________\n',nombre)
    #data=pd.read_csv(f'{nombre}')#Es el archivo generado en "read_stars_v2mod"desde el correspondiente archivo binario
    data=pd.read_csv(nombre)
    data=data.loc[:,['ID','POS_X','POS_Y','POS_Z','VEL_X','VEL_Y','VEL_Z','INIT_MASS','AGE','X_SNII','X_SNIa1','MASS_PARTICLE']]
    
    tamaño=int(nombre[-13:-11]) 
        
    tamaño=int(tamaño/2)
    
    MaX=tamaño
    MiX=-tamaño
    MaY=tamaño
    MiY=-tamaño
    MaZ=tamaño
    MiZ=-tamaño
    data = data[(data['POS_X']<=MaX)& (data['POS_X']>=MiX)&(data['POS_Y']<=MaY)& (data['POS_Y']>=MiY)&(data['POS_Z']<=MaZ)& (data['POS_Z']>=MiZ)]
    
    
    Nit=1
    
    for i in range(0,Nit,1):
        cm=CM2()
        cmX=cm[0]
        cmY=cm[1]
        cmZ=cm[2]
        
        arreglo_rmt=distribucion(cmX,cmY,cmZ,data,tamaño)
        
        #el arregloE_M = arreglo3, es una matriz de 30*2. Cada fila representa la cantidad de estrellas en su intervalo de ancho dr
        DF=pd.DataFrame(arreglo_rmt,columns=['r','masa_acumulada','masa_dr','estrella_dr'])
        radio=radio_virial(tamaño, DF)
        
    
    
    nombre=str(nombre)
    nombre=nombre[-21:]
    
    plt.figure(1)
    DF.plot(x = 'r', y = 'masa_acumulada', kind = 'scatter' )
    plt.ylabel('masa_acumulada [Msol]')
    plt.xlabel('r [Kpc]')
    plt.title(nombre)
    plt.plot(radio[0],radio[2],marker='o',color='r') 
    dataRcm=data[(((data['POS_X']-cmX)*(data['POS_X']-cmX)+(data['POS_Y']-cmY)*(data['POS_Y']-cmY)+(data['POS_Z']-cmZ)*(data['POS_Z']-cmZ))<radio[0]*radio[0])]
    SFR=tasa_estelar(dataRcm,radio[2])#devuelve (SFR,SFRe,masa de estrellas jovenes)
    
    if (galaxia_lista==False and demo==False):
       
        dataRcm=dataRcm.loc[:,['ID','POS_X','POS_Y','POS_Z','MASS_PARTICLE']]
        dataRcm2=data[(((data['POS_X']-cmX)*(data['POS_X']-cmX)+(data['POS_Y']-cmY)*(data['POS_Y']-cmY)+(data['POS_Z']-cmZ)*(data['POS_Z']-cmZ))<25*radio[0]*radio[0])]
        N=len(DF)
        log_radio=np.zeros([N,1])
        log_masa=np.zeros([N,1])
        cont=0
        for i in range(0,N,1):
            if arreglo_rmt[i,1]!=0:
                log_radio[i]=math.log10(arreglo_rmt[i,0])
                log_masa[i]=math.log10(arreglo_rmt[i,1])
            else:
                cont=cont+1
        N2=N-cont
        log_radio2=np.zeros([N2,1])
        log_masa2=np.zeros([N2,1])
        
        for i in range(0,N2,1):
            log_radio2[i]=log_radio[i+cont]
            log_masa2[i]=log_masa[i+cont]
        plt.figure(1)
        plt.scatter(log_masa2,log_radio2,marker='.',color='k',alpha=1)
        plt.title(nombre)
        plt.xlabel('log masa [log Msol]')
        plt.ylabel('log radio [Kpc]')
        plt.plot(math.log10(radio[2]),math.log10(radio[0]),marker='o',color='r')
        
        
        DF.plot(x = 'r', y = 'masa_acumulada', kind = 'scatter' )
        plt.ylabel('masa_acumulada [Msol]')
        plt.xlabel('r [Kpc]')
        plt.title(nombre)
        plt.plot(radio[0],radio[2],marker='o',color='r')
        plt.plot(radio[1],radio[2]/2,marker='o',color='k')
        
        dataRcm2.plot( x='POS_X',y='POS_Y',kind='scatter',marker='.', alpha=0.1)
        plt.plot(cmX,cmY,marker='o',color='r')
        plt.title(nombre)
        plt.ylabel('Y [Kpc]')
        plt.xlabel('X [Kpc]')
        plt.plot(cmX+radio[0],cmY,marker='.',color='r',alpha=1)
        plt.plot(cmX-radio[0],cmY,marker='.',color='r',alpha=1)
        plt.plot(cmX,cmY+radio[0],marker='.',color='r',alpha=1)
        plt.plot(cmX,cmY-radio[0],marker='.',color='r',alpha=1)
        
        dataRcm2.plot( x='POS_X',y='POS_Z',kind='scatter',marker='.',color='g', alpha=0.1)
        plt.plot(cmX,cmZ,marker='o',color='r')
        plt.title(nombre)
        plt.ylabel('Z [Kpc]')
        plt.xlabel('X [Kpc]')
        plt.plot(cmX+radio[0],cmZ,marker='.',color='r',alpha=1)
        plt.plot(cmX-radio[0],cmZ,marker='.',color='r',alpha=1)
        plt.plot(cmX,cmZ+radio[0],marker='.',color='r',alpha=1)
        plt.plot(cmX,cmZ-radio[0],marker='.',color='r',alpha=1)
        
        dataRcm2.plot( x='POS_Y',y='POS_Z',kind='scatter',marker='.',color='k', alpha=0.1)
        plt.plot(cmY,cmZ,marker='o',color='r')
        plt.plot(cmY+radio[0],cmZ,marker='.',color='r',alpha=1)
        plt.plot(cmY-radio[0],cmZ,marker='.',color='r',alpha=1)
        plt.plot(cmY,cmZ+radio[0],marker='.',color='r',alpha=1)
        plt.plot(cmY,cmZ-radio[0],marker='.',color='r',alpha=1)
        plt.title(nombre)
        plt.ylabel('Z [Kpc]')
        plt.xlabel('Y [Kpc]')
    return(cmX,cmY,cmZ,radio[2],radio[0],radio[1],SFR[0],SFR[1],SFR[2])  