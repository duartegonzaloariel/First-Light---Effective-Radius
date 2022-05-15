# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 15:18:03 2021

@author: GONZALO DUARTE
"""
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import pylab
import time


#____________________________lista de masas_________________
def lista_masas(data,tamaño):
    tamaño1=tamaño
    arreglo=np.zeros([3,3,3])
    arreglo2=np.zeros([3,1])
    MaX=tamaño1
    MiX=-tamaño1
    MaY=tamaño1
    MiY=-tamaño1
    MaZ=tamaño1
    MiZ=-tamaño1
    N1=0.01
    N2=int((math.log10(tamaño1/N1))/math.log10(3))
    
    #print(N2)
    A=(MaY-MiY)
    for l in range(0,N2,1):
        for i in range(0,3,1):
            for j in range(0,3,1):
                for k in range(0,3,1):
                    arreglo[i,j,k]=len(data[(data['POS_X']>(MiX +2*k*tamaño1/3)) & (data['POS_X']<(MiX +2*(k+1)*tamaño1/3)) & (data['POS_Y']>(MiY +2*j*tamaño1/3)) & (data['POS_Y']<(MiY +2*(j+1)*tamaño1/3))&(data['POS_Z']>(MiZ +2*i*tamaño1/3)) & (data['POS_Z']<(MiZ +2*(i+1)*tamaño1/3))])
        N=np.amax(arreglo)
        for i in range(0,3,1):
            for j in range(0,3,1):
                for k in range(0,3,1):
                    if arreglo[i,j,k]==N:
                        arreglo2[0,0]=k
                        arreglo2[1,0]=j
                        arreglo2[2,0]=i
        
        if arreglo2[0,0]==0:
            MaX=MiX+A*2/6
            MiX=MiX
        else:
            if arreglo2[0,0]==1:
                MaX=MiX+A*4/6
                MiX=MiX+A*2/6
            else:
                MaX=MaX
                MiX=MiX+A*4/6
        
        if arreglo2[1,0]==0:
            MaY=MiY+A*2/6
            MiY=MiY
        else:
            if arreglo2[1,0]==1:
                MaY=MiY+A*4/6
                MiY=MiY+A*2/6
            else:
                MaY=MaY
                MiY=MiY+A*4/6
        
        if arreglo2[2,0]==0:
            MaZ=MiZ+A*2/6
            MiZ=MiZ
        else:
            if arreglo2[2,0]==1:
                MaZ=MiZ+A*4/6
                MiZ=MiZ+A*2/6
            else:
                MaZ=MaZ
                MiZ=MiZ+A*4/6
        A=(MaY-MiY)        
        tamaño1=A/2
        
    #print(arreglo2)
    return(MaX,MiX,MaY,MiY,MaZ,MiZ)


    
#___________________________Calculo del centro de masa 1_________________________

def CM(MaX,MiX,MaY,MiY,MaZ,MiZ,data,R):
    x=(MaX+MiX)/2
    y=(MaY+MiY)/2
    z=(MaZ+MiZ)/2
    
    dataR = data[(data['POS_X']<=R+x)& (data['POS_X']>=(-R+x)) & (data['POS_Y']<=R+y) & (data['POS_Y']>=(-R+y))&(data['POS_Z']<=R+z)& (data['POS_Z']>=(-R+z))]
    dataR =dataR.drop(['VEL_X','VEL_Y','VEL_Z','INIT_MASS','AGE','X_SNII','X_SNIa1'],axis=1)
    arreglo = np.array(dataR)
    N=len(dataR)
    #print('\n-----------------------------------------------\n\ndentro de un radio de',R,'kpcs, hay',N,'estrellas')
    X=0
    Y=0
    Z=0
    M=0
    for k in range(0,N,1):
        X=X+(arreglo[k,4])*(arreglo[k,1])
        Y=Y+(arreglo[k,4])*(arreglo[k,2])
        Z=Z+(arreglo[k,4])*(arreglo[k,3])
        M=M+(arreglo[k,4])
        
    cmX=X/M
    cmY=Y/M
    cmZ=Z/M
    #print('\nlas coordenadasdel centro de masa son:','\ncmX=',cmX,'\ncmY=',cmY,'\ncmZ=',cmZ)
    return(cmX,cmY,cmZ)

#___________________________Calculo del centro de masa 2_________________________

def CM2():
        
    cmX=0
    cmY=0
    cmZ=0
    return(cmX,cmY,cmZ)


#___________________________Calculo de distribucion de masas___________________

def distribucion(cmX,cmY,cmZ,data,tamaño):
    dr=0.02
    R2=tamaño# "R2" debe ser tal que al multiplicar por "dr" de un numero entero. ya que define la cantidad de filas de "arreglo3"
    dataRcm=data[(((data['POS_X']-cmX)*(data['POS_X']-cmX)+(data['POS_Y']-cmY)*(data['POS_Y']-cmY)+(data['POS_Z']-cmZ)*(data['POS_Z']-cmZ))<=R2*R2)]
    dataRcm=dataRcm.drop(['ID','VEL_X','VEL_Y','VEL_Z','INIT_MASS','AGE','X_SNII','X_SNIa1'],axis=1)
    
    N3=int(R2/dr)
   
    arreglo3=np.zeros([N3,4])
    
    for j in range(0,N3,1):
        masa=0
        dataRcm2=dataRcm[(((dataRcm['POS_X']-cmX)*(dataRcm['POS_X']-cmX)+(dataRcm['POS_Y']-cmY)*(dataRcm['POS_Y']-cmY)+(dataRcm['POS_Z']-cmZ)*(dataRcm['POS_Z']-cmZ))<((j+1)*dr)*((j+1)*dr))]
        dataRcm=dataRcm[(((dataRcm['POS_X']-cmX)*(dataRcm['POS_X']-cmX)+(dataRcm['POS_Y']-cmY)*(dataRcm['POS_Y']-cmY)+(dataRcm['POS_Z']-cmZ)*(dataRcm['POS_Z']-cmZ))>=((j+1)*dr)*((j+1)*dr))]
        N2=len(dataRcm2)
        arreglo2=np.array(dataRcm2)
        for i in range(0,N2,1):
            masa=masa+arreglo2[i,3]
        arreglo3[j,3]=N2
        arreglo3[j,2]=masa
        arreglo3[j,0]=(j+1)*dr
    arreglo3[0,1]=arreglo3[0,1]+arreglo3[0,2]
    for l in range(1,N3,1):
        arreglo3[l,1]= arreglo3[l,2]+arreglo3[(l-1),1]
        
    #print('\n',arreglo3)
    return(arreglo3)


#____________________________busca radio donde cambia la pendiente_____________
#"""
def cambia_pendiente(DF,factor,R2):
    xy=np.array(DF)
    
    N=len(xy)
    
    lugar=0
    N2=int(N/6)
    control=0
    control2=0
    
    if R2==0:
        for i in range(N2,N-2,1):
            
            if ( (1* (xy[i+1,1]-xy[i+0,1])/(xy[i+1,0]-xy[i+0,0]) )>( (xy[i+2,1]-xy[i+1,1])/(xy[i+2,0]-xy[i+1,0]) )):
                lugar=i+1
                #if ( (1* (xy[i+2,1]-xy[i+1,1])/(xy[i+2,0]-xy[i+1,0]) )>( (xy[i+3,1]-xy[i+2,1])/(xy[i+3,0]-xy[i+2,0]) )):
                    #lugar=i+1
                    #if ( (1* (xy[i+3,1]-xy[i+2,1])/(xy[i+3,0]-xy[i+2,0]) )>( (xy[i+4,1]-xy[i+3,1])/(xy[i+4,0]-xy[i+3,0]) )):
                        #lugar=i+1
            if lugar !=0:
                break
    else:
       
       for j in range(0,N,1):
           if xy[j,0]<=R2:
               lugar=j
           else:
               break
       for k in range(lugar,N-1,1):
           if (((xy[lugar,1]-xy[lugar-1,1])*factor) <= (xy[k+1,1]-xy[k,1])):
               control2=k-lugar
               control=0
           else:
               control=control+1
           if control==2:
               break
                            
    lugar=lugar+control2       
    radio=xy[lugar,0]
    masa=xy[lugar,1]
    masa_e=0
    radio_ef=0
    k=0
    while masa_e<masa/2:
        masa_e=xy[k,1]
        k=k+1# al salir del while esta en k+1 que no se computo, ver notas 22-4
    radio_ef=xy[k-1,0]# en el codigo anterior falta restar 1
    
    
    return(radio,radio_ef,masa)


#____________________________busca radio 2_____________
#"""
def radio_virial (tamaño, DF):
    xy=np.array(DF)
    N=len(xy)
     
    radio=tamaño/2
    
    for j in range(0,N,1):
           if xy[j,0]<=radio:
               lugar=j
           else:
               break
           
    masa=xy[lugar,1]
    masa_e=0
    radio_ef=0
    k=0
    while masa_e<masa/2:
         masa_e=xy[k,1]
         k=k+1
    radio_ef=xy[k-1,0]
    return(radio,radio_ef,masa)


#____________________________tasa de formacion estelar_________________________
    
def tasa_estelar(data,masa):
    
       
    estrella_nueva=data[((data['AGE'])<=0.03)]
    estrella_nueva=estrella_nueva.loc[:,['MASS_PARTICLE']]
    arreglo3=np.array(estrella_nueva)
    
    N3=len(estrella_nueva)
    N4=0.0
    for i in range(0,N3,1):
        N4=N4+arreglo3[i,0]#el ",0]" espara que devuelva un numero y no un "[XXXX.XXXX]"
    SFR=N4/0.03#masa total de estrellas menores a 30.000 años dividido el radio de la galaxia
    SFRe=SFR/masa
   
    return(SFR,SFRe,N4)#N4 es la masa total de estrellas menores a 30.000 años