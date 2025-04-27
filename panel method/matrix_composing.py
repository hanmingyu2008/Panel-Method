import numpy as np
import math
from geometry import strengths_group_edge
import airfoil
import landscape

def matrix_contribution(foil, anafoil, alpha, Vinf):
    # foil的foil.Num+1个属性对 anafoil的airfoil2.Num+1个方程的贡献
    N,Na = foil.Num, anafoil.Num
    Ts,Ns,Tv,Nv=strengths_group_edge(anafoil.edges, foil, device="cpu")
    # 以上应该是Na行,N列的矩阵们(不看第0行和第0列)
    
    Leng,Sine,Cosi = anafoil.Leng,anafoil.Sine,anafoil.Cosi
    A = np.zeros((Na+2, N+2))
    for i in range(1, Na+1):
        temp = 0
        for j in range(1, N+1):
            A[i][j] = Ns[i][j]
            temp += Nv[i][j]
        A[i][N+1] = temp
    temp1,tempn = 0,0 
    for j in range(1, N+1):
        A[Na+1][j] = Ts[1][j]+Ts[Na][j]
        temp1 += Tv[1][j]
        tempn += Tv[Na][j]
    A[Na+1][N+1] = temp1+tempn

    return A[1:,1:],Ts,Ns,Tv,Nv

def vector_contribution(anafoil, alpha, Vinf):
    Na = anafoil.Num
    Leng,Sine,Cosi = anafoil.Leng,anafoil.Sine,anafoil.Cosi
    b = np.zeros(Na+2)
    for i in range(1, Na+1):
        b[i] = -Vinf*(Cosi[i]*math.sin(alpha)-Sine[i]*math.cos(alpha))
    b[Na+1] = -Vinf*((Cosi[1]+Cosi[Na])*math.cos(alpha)+(Sine[1]+Sine[Na])*math.sin(alpha))
    return b[1:]