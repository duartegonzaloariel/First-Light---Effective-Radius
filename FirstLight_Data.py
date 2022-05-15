# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 18:44:00 2021

@author: GONZALO DUARTE
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import pylab
import time

#____________________________lista de trabajo_________________

def listas(demo):
    
    if demo==True:
        lista=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\listas\demo.csv"
    else:    
        nombre_lista=input('seleccione:\n1 para z6\n2 para z10\n3 para 836\n4 para 851\n5 para 884\n6 para 893\n7 para 915\n8 para 946\n')
          #lista=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\listas\lista_demo.csv"
            
        nombre_lista=int(nombre_lista)
        if nombre_lista==1:
            lista=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\listas\z06.csv"  
        elif nombre_lista==2:
            lista=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\listas\z10.csv"
        elif nombre_lista==3:
            lista=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\listas\836.csv"
        elif nombre_lista==4:
            lista=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\listas\851.csv"
        elif nombre_lista==5:
            lista=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\listas\884.csv"
        elif nombre_lista==6:
            lista=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\listas\893.csv"
        elif nombre_lista==7:
            lista=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\listas\915.csv"
        elif nombre_lista==8:
            lista=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\listas\946.csv"
        else:
            print('lista incorrecta, se ejecurara la lista demo')
            lista=r"C:\Users\GONZALO\Desktop\IAlpha_DataScience\Tabajos\IA_galaxias\galaxias_master\listas\demo.csv"  
    return(lista)