import numpy as np
import math
import torch
from solverN import solverN_traditional
from solver import solver_traditional
import airfoil
import landscape

namelist = input("input namelist of airfoils: ").split()
NNN = len(namelist)
quiet = True
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

foils = [None]
for name in namelist:
    load_properties=np.load("properties/"+name+"_properties.npz")
    coorX = load_properties["coorX"]
    coorY = load_properties["coorY"]
    foils.append(airfoil.listtofoil(coorX,coorY))

alpha = 0    #alpha是倾斜角 (充分远处的"自由流"的倾斜角)
Vinf = 1


landsc = landscape.landscape(foils)
Ut,Un,Cp,q = solverN_traditional(landsc, alpha, Vinf)
for i in range(1,NNN+1):
    print(q[i][-1])
for i in range(1,NNN+1):
    with open("cp"+str(i)+".dat","w") as file:
        for t in range(1,len(Cp[i])):
            print(Cp[i][t],file=file)
nami = ''
for i in range(NNN):
    if i<NNN-1:
        nami += namelist[i]+"+"
    else:
        nami += namelist[i]

save_q = {
    f'q{i}': q[i][:-1] 
    for i in range(1, len(q))  # 跳过第0项（None），从1开始
}

save_Ut = {
    f'Ut{i}': Ut[i]
    for i in range(1, len(Ut))  # 跳过第0项（None），从1开始
}

save_Cp = {
    f'Cp{i}': Cp[i]
    for i in range(1, len(Cp))  # 跳过第0项（None），从1开始
}

save_gamma = {
    f'gamma{i}': q[i][-1]
    for i in range(1, len(q))  # 跳过第0项（None），从1开始
}

np.savez("data/"+nami+"_data.npz",**save_q,**save_gamma,**save_Cp,**save_Ut)