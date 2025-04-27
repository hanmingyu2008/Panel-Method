import numpy as np
import math
import torch
from solverN import solverN_traditional
from solver import solver_traditional
import airfoil
import landscape

name1 = input("input name of airfoil model1: ")
name2 = input("input name of airfoil model2: ")
quiet = True
load_properties1 = np.load("properties/"+name1+'_properties.npz')
load_properties2 = np.load("properties/"+name2+'_properties.npz')
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

#注意，一下涉及到的角标全都从1开始数，也就是说前面会多一个0。
N1 = load_properties1['N']    #点的个数(1和N+1是一个)
# Vinf = load_properties['Vinf']  #V_\infty (充分远处的"自由流"的速度)
#为了周期边界条件的处理方便，我们的角标记录N+1个(1和N+1是一个)，故coorX和coorY都是N+2维的
coorX1 = load_properties1['coorX']    #第i个点坐标[xi,yi]分别存储在coorX和coorY中
coorY1 = load_properties1['coorY'] 
N2 = load_properties2["N"]
coorX2 = load_properties2['coorX']    #第i个点坐标[xi,yi]分别存储在coorX和coorY中
coorY2 = load_properties2['coorY']  
alpha = 0    #alpha是倾斜角 (充分远处的"自由流"的倾斜角)
Vinf = 1



foil1,foil2 = airfoil.listtofoil(coorX1,coorY1),airfoil.listtofoil(coorX2,coorY2)
landsc = landscape.landscape([None,foil1,foil2])
Ut,Un,Cp,q = solverN_traditional(landsc, alpha, Vinf, device)
print(q[1][-1],q[2][-1])
for i in range(1,3):
    with open("cp"+str(i)+".dat","w") as file:
        for t in range(1,len(Cp[i])):
            print(Cp[i][t],file=file)
# np.savez("data/"+name+"_data.npz",Ut=Ut,Un=Un,Cp=Cp,Q=Q,Gamma=Gamma)