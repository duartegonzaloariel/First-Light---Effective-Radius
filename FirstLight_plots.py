# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 22:51:54 2020

@author: GONZALO DUARTE
"""
import pandas as pd
import numpy as np
import math 

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import timeit
start=timeit.timeit()

##############################################################################
#  Selection model and galaxy
##############################################################################
galaxy_study='model_1_884.csv'


data=pd.read_csv(galaxy_study)
N=len(data)
arreglo=np.array(data)
log_radioe=np.zeros([N,1])
radioe=np.zeros([N,1])
log_masa=np.zeros([N,1])
log_SFR=np.zeros([N,1])
log_SFRe=np.zeros([N,1])
z=np.zeros([N,1])
log_control=np.zeros([48,1])
masax=np.zeros([48,1])

for i in range(0,N,1):
    log_radioe[i]=math.log10(arreglo[i,6])
    radioe[i]=arreglo[i,6]
    log_masa[i]=math.log10(arreglo[i,4])
    log_SFR[i]=math.log10((arreglo[i,7])/1000000000)# en 'resultados_z10.csv', SFR esta en [Msol/Gyr]
    log_SFRe[i]=math.log10((arreglo[i,8])/1000000000)#  en 'resultados_z10.csv', SFRe esta en [1/Gyr]
    nombre=arreglo[i,0]
    z[i]=1/(float(nombre[12:17]))-1#calculo de z desde el factor de escala en el nombre del archivo
    #print(nombre[12:17]) Control del factor de escala

##############################################################################
#  Plos Ref-Mas-sSFR, Ref-Mas-Z, 
##############################################################################
galaxy_study=galaxy_study[:-4]#Title without .csv

plt.figure(1)
#plt.scatter(log_masa,log_radioe,c=log_SFRe,marker='.', s=100, alpha=0.8, cmap='jet_r', label='vela')
plt.scatter(log_masa,radioe,c=log_SFRe,marker='.', s=200,linewidth=2, alpha=0.5, cmap='jet_r', label='vela')
plt.colorbar(label='sSFR')#el$ hace que el "_"indique subindice
plt.scatter(masax,log_control,marker='.',color='r',alpha=1)
plt.xlim(6,10)
plt.ylim((10**(-1.4)),(10**(1)))
plt.title(galaxy_study,size=15)
plt.xlabel('log($M_*$/$M_{SUM}$)',size=15)
plt.ylabel('R$_e$$_f$ [Kpcs]',size=15)
plt.yscale('log')

plt.figure(2)
#plt.scatter(log_masa,log_radioe,c=z,marker='.', s=100, alpha=0.8, cmap='jet_r', label='vela')
plt.scatter(log_masa,radioe,c=z,marker='.', s=200, linewidth=2, alpha=0.5, cmap='jet_r', label='vela')
plt.colorbar(label='z')#el$ hace que el "_"indique subindice
plt.scatter(masax,log_control,marker='.',color='r',alpha=1)
plt.xlim(6,10)
plt.ylim((10**(-1.4)),(10**(1)))
plt.title(galaxy_study,size=15)
plt.xlabel('log($M_*$/$M_{SUM}$)',size=15)
plt.ylabel('R$_e$$_f$ [Kpcs]',size=15)
plt.yscale('log')

plt.figure(3)
plt.scatter(log_masa,log_SFR,marker='.',s=200,linewidth=2,color='r',alpha=0.5)
plt.xlim(6,10)
plt.ylim(-3.5,1.5)
plt.title(galaxy_study,size=15)
plt.xlabel('log($M_*$/$M_{SUM}$)',size=15)
plt.ylabel('log($SFR$/$(M_{SUM}yr^{-1})$)',size=15)

plt.figure(4)
plt.scatter(log_masa,log_SFRe,marker='.',s=200,linewidth=2,color='m',alpha=0.5)
plt.xlim(6,10)
plt.ylim(-10.5,-7)
plt.title(galaxy_study,size=15)
plt.xlabel('log($M_*$/$M_{SUM}$)',size=15)
plt.ylabel('log($sSFR$/$(M_{SUM}yr^{-1})$)',size=15)
end=timeit.timeit()
