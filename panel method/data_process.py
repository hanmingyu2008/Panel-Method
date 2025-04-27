import numpy as np
import math
import torch
from solverN import solverN_traditional
from solver import solver_traditional
import airfoil
import landscape

name = input("input name of airfoil model1: ")
quiet = True
load_properties = np.load("properties/"+name+'_properties.npz')
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

#注意，一下涉及到的角标全都从1开始数，也就是说前面会多一个0。
N = load_properties['N']    #点的个数(1和N+1是一个)
# Vinf = load_properties['Vinf']  #V_\infty (充分远处的"自由流"的速度)
#为了周期边界条件的处理方便，我们的角标记录N+1个(1和N+1是一个)，故coorX和coorY都是N+2维的
coorX = load_properties['coorX']    #第i个点坐标[xi,yi]分别存储在coorX和coorY中
coorY = load_properties['coorY']  
alpha = 0    #alpha是倾斜角 (充分远处的"自由流"的倾斜角)
Vinf = 1



foil = airfoil.listtofoil(coorX,coorY)
landsc = landscape.landscape([None,foil])
Ut,Un,Cp,q = solverN_traditional(landsc, alpha, Vinf, device)
Ut=Ut[1]
Un=Un[1]
Cp=Cp[1]
with open("cp"+".dat","w") as file:
    for t in range(1,len(Cp)):
        print(Cp[t],file=file)
np.savez("data/"+name+"_data.npz",Ut=Ut,Un=Un,Cp=Cp,Q=q[:-1],Gamma=q[-1])