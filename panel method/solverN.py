import numpy as np
import math
from geometry import strengths_group_edge
import airfoil
from matrix_composing import matrix_contribution,vector_contribution

def solverN_traditional(landsc, alpha, Vinf, req="quiet", only_q=False):
    A = np.zeros((landsc.totlength+1,landsc.totlength+1))
    b = np.zeros(landsc.totlength+1)
    Ts = [[None for _ in range(landsc.size+1)] for _ in range(landsc.size+1)]
    Ns = [[None for _ in range(landsc.size+1)] for _ in range(landsc.size+1)]
    Tv = [[None for _ in range(landsc.size+1)] for _ in range(landsc.size+1)]
    Nv = [[None for _ in range(landsc.size+1)] for _ in range(landsc.size+1)]

    for i in range(1,landsc.size+1):
        stonei = landsc.templist[i]
        for j in range(1,landsc.size+1):
            stonej = landsc.templist[j]
            A[stonei+1:stonei+landsc.Numlist[i]+2,stonej+1:stonej+landsc.Numlist[j]+2],\
                 Ts[i][j],Ns[i][j],Tv[i][j],Nv[i][j] = \
                    matrix_contribution(landsc.foils[j],landsc.foils[i],alpha,Vinf)
            '''
            with open("Ts"+str(i)+str(j)+".dat","w") as file:
                for k in range(1,landsc.Numlist[i]+1):
                    for l in range(1,landsc.Numlist[j]+1):
                        print(Ts[i][j][k][l].item(),end=" ",file=file)
                    print("",file=file)'''
            '''
            with open("Tv"+str(i)+str(j)+".dat","w") as file:
                for k in range(1,landsc.Numlist[i]+1):
                    for l in range(1,landsc.Numlist[j]+1):
                        print(Tv[i][j][k][l].item(),end=" ",file=file)
                    print("",file=file)'''
            '''
            with open("Ns"+str(i)+str(j)+".dat","w") as file:
                for k in range(1,landsc.Numlist[i]+1):
                    for l in range(1,landsc.Numlist[j]+1):
                        print(Ns[i][j][k][l].item(),end=" ",file=file)
                    print("",file=file)
            with open("Nv"+str(i)+str(j)+".dat","w") as file:
                for k in range(1,landsc.Numlist[i]+1):
                    for l in range(1,landsc.Numlist[j]+1):
                        print(Nv[i][j][k][l].item(),end=" ",file=file)
                    print("",file=file)'''
        b[stonei+1:stonei+landsc.Numlist[i]+2] = \
                vector_contribution(landsc.foils[i],alpha,Vinf)
    
    with open("A.dat","w") as file:
        for k in range(1,landsc.totlength+1):
            for l in range(1,landsc.totlength+1):
                print(A[k][l],end=" ",file=file)
            print("",file=file)
    with open("b.dat","w") as file:
        for k in range(1,landsc.totlength+1):
            print(b[k],file=file)

    QQ = np.zeros(landsc.totlength+1)
    QQ[1:landsc.totlength+1] = \
        np.linalg.solve(A[1:landsc.totlength+1,1:landsc.totlength+1], b[1:landsc.totlength+1])
    '''
    with open("QQ.dat","w") as file:
        for i in range(1,landsc.totlength+1):
            print(QQ[i],file=file)'''
    if not only_q:
        q = [None for _ in range(landsc.size+1)]
        ut = [None for _ in range(landsc.size+1)]
        un = [None for _ in range(landsc.size+1)]
        Cp = [None for _ in range(landsc.size+1)]
        for i in range(1,landsc.size+1):
            foil = landsc.foils[i]
            N = foil.Num
            q[i] = np.zeros(N+2)
            q[i][1:] = QQ[landsc.templist[i]+1:landsc.templist[i]+landsc.Numlist[i]+2]
            ut[i] = np.zeros(N+1)
            un[i] = np.zeros(N+1)
            Cosi,Sine = foil.Cosi,foil.Sine
            for j in range(1,N+1):
                ut[i][j] = Vinf*(math.cos(alpha)*Cosi[j]+math.sin(alpha)*Sine[j])
                un[i][j] = Vinf*(-math.cos(alpha)*Sine[j]+math.sin(alpha)*Cosi[j])
        for ii in range(1,landsc.size+1):
            N1 = landsc.foils[ii].Num
            for jj in range(1,landsc.size+1):
                N2 = landsc.foils[jj].Num
                for i in range(1, N1+1):
                    for j in range(1, N2+1):
                        ut[ii][i] += Ts[ii][jj][i][j]*q[jj][j]+Tv[ii][jj][i][j]*q[jj][-1]
                        un[ii][i] += Ns[ii][jj][i][j]*q[jj][j]+Nv[ii][jj][i][j]*q[jj][-1]
        for ii in range(1,landsc.size+1):
            N = landsc.foils[ii].Num
            # print(q[ii][-1])
            Cp[ii] = np.zeros(N+1)
            for i in range(1,N+1):
                Cp[ii][i] = 1-(ut[ii][i]/Vinf)**2
                if abs(un[ii][i])>1e-5:
                    print("boundary flow condition isn't satisfied!")
        return ut,un,Cp,q
    else:
        q = [None for _ in range(landsc.size+1)]
        for i in range(1,landsc.size+1):
            foil = landsc.foils[i]
            N = foil.Num
            q[i] = np.zeros(N+2)
            q[i][1:] = QQ[landsc.templist[i]+1:landsc.templist[i]+landsc.Numlist[i]+2]
        return q