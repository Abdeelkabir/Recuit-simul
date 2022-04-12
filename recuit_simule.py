# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 21:30:53 2022

@author: HP
"""

import time
import random
import math
import numpy as np
import matplotlib.pyplot as plt
#------------------------------------------------------------------------------
# Section de personnalisation :
temp_initial = 100
refroid = 0.8  # coefficient de refroidissement
nb_var = 2
UB = [3, 3]   #limites supérieur
LB = [-3, -3]  #limites inférieures
tps = 1 # calcul de temps par seconde

#définition de la fonction objective
def obj_func(X):
    x=X[0]
    y=X[1]
    val = 3*(1-x)**2*math.exp(-x**2 - (y+1)**2) - 10*(x/5 - x**3 - y**5)*math.exp(-x**2 - y**2) -1/3*math.exp(-(x+1)**2 - y**2)
    return val
  
#------------------------------------------------------------------------------
#Algorithme de récuit simulé
sol_initial=np.zeros((nb_var))
for i in range(nb_var):
    sol_initial[i] = random.uniform(LB[i],UB[i])
      
sol_actuelle = sol_initial
sol_meill = sol_initial
n = 1  # nb de solutions acceptées
BF = obj_func(sol_meill)
temp_act = temp_initial # temperature courante
debut = time.time()
nb_attem = 100 # nombre de tentatives dans chaque niveau de température
rbf =[]
  
for i in range(9999999):
    for j in range(nb_attem):
  
        for k in range(nb_var):
            sol_actuelle[k] = sol_meill[k] + 0.1*(random.uniform(LB[k],UB[k]))
            sol_actuelle[k] = max(min(sol_actuelle[k], UB[k]), LB[k])

        CF = obj_func(sol_actuelle)
        E = abs(CF - BF)
        if i == 0 and j == 0 :
            EA = E
        
        if CF < BF:
            p = math.exp(-E/EA*temp_act)
            # prendre la décision d’accepter la pire solution ou non
            if random.random()<p:
                ACCEPT=True # Cette pire solution est acceptée
            else:
                ACCEPT = False # Cette pire solution n’est pas acceptée

        else:
            ACCEPT = True # accepter une meilleure solution
        
        if ACCEPT == True:
            sol_meill = sol_actuelle # mettre à jour la meilleure solution
            BF = obj_func(sol_meill)
            n = n + 1 # compter la solution acceptée
            EA = (EA * (n-1) + E)/n # modofier EA
        
    print('iteration:{},Meilleur solution: {}, Meilleur fitness: {}'.format(i, sol_meill, BF))
    rbf.append(BF)
    # Refroidissement de la température
    temp_act = temp_act * refroid

    fin = time.time()
    if fin-debut >= tps:
        break

plt.plot(rbf)
plt.show()
