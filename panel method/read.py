import numpy as np
import math
import random

namelist = input("input name of airfoil model:").split()
req_gap = input("do you need a gap? yes or no: ")

for name in namelist:
    coorX = [0]
    coorY = [0]

    with open("mesh/"+name+"_mesh.dat", "r") as file:
        lines = file.readlines()
        for line in lines:
            ls = [float(x) for x in line.split()]
            x,y = ls[0],ls[1]
            coorX.append(x)
            coorY.append(y)
    if req_gap=="no":
        coorX.append(coorX[1])
        coorY.append(coorY[1])
    coorX = np.array(coorX)
    coorY = np.array(coorY)
    N = len(coorX)-2
    Vinf = 1
    np.savez_compressed("properties/"+name+"_properties.npz",coorX=coorX,coorY=coorY,N=N,
                        Vinf=Vinf)