# 使用传统的PanelMethod求解“无粘不可压缩势流”
# 针对翼型是非闭合的折线类型
import numpy as np
import math
import torch
from geometry import strengths_group_edge
import airfoil

def solver_traditional(foil, alpha, Vinf, device, req="quiet"):
    coorX = [None]
    coorY = [None]
    for i in range(1,foil.Num+2):
        coorX.append(foil.points[i].x)
        coorY.append(foil.points[i].y)

    N = len(coorX)-2

    if req!="quiet":
        print('start solving')
        print("N=",N,",V_inf=",Vinf,",len(coorX)=",len(coorX),",len(coorY)=",len(coorY),",alpha=",alpha)

    Ts,Ns,Tv,Nv=strengths_group_edge(foil.edges, foil, device="cpu")
    '''
    with open("Us.dat","w") as file:
        for i in range(1,N+1):
            for j in range(1,N+1):
                print(Us[i][j].item(),end=" ",file=file)
            print("",file=file)
    with open("Uv.dat","w") as file:
        for i in range(1,N+1):
            for j in range(1,N+1):
                print(Uv[i][j].item(),end=" ",file=file)
            print("",file=file)    
    with open("Vs.dat","w") as file:
        for i in range(1,N+1):
            for j in range(1,N+1):
                print(Vs[i][j].item(),end=" ",file=file)
            print("",file=file)  
    with open("Vv.dat","w") as file:
        for i in range(1,N+1):
            for j in range(1,N+1):
                print(Vv[i][j].item(),end=" ",file=file)
            print("",file=file)'''
    Leng,Sine,Cosi = foil.Leng,foil.Sine,foil.Cosi
    A = torch.zeros((N+2, N+2),device=device)
    b = torch.zeros(N+2,device=device)
    for i in range(1, N+1):
        temp = 0
        for j in range(1, N+1):
            A[i][j] = Ns[i][j]
            temp += Nv[i][j]
        A[i][N+1] = temp
        b[i] = -Vinf*(Cosi[i]*math.sin(alpha)-Sine[i]*math.cos(alpha))

    temp1,tempn = 0,0 
    for j in range(1, N+1):
        A[N+1][j] = Ts[1][j]+Ts[N][j]
        temp1 += Tv[1][j]
        tempn += Tv[N][j]
    A[N+1][N+1] = temp1+tempn
    b[N+1] = -Vinf*((Cosi[1]+Cosi[N])*math.cos(alpha)+(Sine[1]+Sine[N])*math.sin(alpha))

    print(torch.norm(A),torch.norm(b))

    
    with open("A.dat","w") as file:
        for i in range(1,N+2):
            for j in range(1,N+2):
                print(A[i][j].item(),end=" ",file=file)
            print("",file=file)

    if req!="quiet":
        print("norm(A)=",torch.norm(A),",norm(b)=",torch.norm(b))

        print("finished composing matrix")

    q = torch.zeros(N+2,device=device)
    q[1:N+2] = torch.linalg.solve(A[1:N+2, 1:N+2], b[1:N+2])
    gamma = q[N+1]

    with open("q2"+".dat","w") as file :
            for t in range(1,N+2):
                print(q[t],file=file)
    if req!="quiet":
        print("finished solving NLA system")

    ut = torch.zeros(N+1,device=device)
    un = torch.zeros(N+1,device=device)
    Cp = torch.zeros(N+1,device=device)
    for i in range(1, N+1):
        ut[i] = Vinf*(math.cos(alpha)*Cosi[i]+math.sin(alpha)*Sine[i])
        un[i] = Vinf*(-math.cos(alpha)*Sine[i]+math.sin(alpha)*Cosi[i])
        for j in range(1, N+1):
            ut[i] += Ts[i][j]*q[j]+Tv[i][j]*gamma
            un[i] += Ns[i][j]*q[j]+Nv[i][j]*gamma
        Cp[i] = 1-(ut[i]/Vinf)**2
    for i in range(1,N+1):
        if abs(un[i])>1e-5:
            print("boundary flow condition do not satisfies")
    if req!="quiet":
        print("finished")    
    return ut,un,Cp,q