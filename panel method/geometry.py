import numpy as np
import math
import torch

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class edge:
    #这个边其实是有向的,在机翼上整体来看为顺时针最好
    def __init__(self, p1, p2):
        self.p1,self.p2 = p1,p2
        self.mid = point((p1.x+p2.x)/2,(p1.y+p2.y)/2)
        self.leng = math.sqrt((p2.x-p1.x)**2+(p2.y-p1.y)**2)
        self.sine = (p2.y-p1.y)/self.leng
        self.cosi = (p2.x-p1.x)/self.leng


def strengths_single_point(p, foil, device="cpu"):
    x0, y0 = p.x,p.y
    N = foil.Num
    coorX,coorY = foil.tolist()
    Leng,Sine,Cosi = foil.Leng,foil.Sine,foil.Cosi

    Rlen = torch.zeros(N+2, device=device)
    for j in range(1, N+2):
        Rlen[j] = math.sqrt((x0-coorX[j])**2+(y0-coorY[j])**2)
    SineBeta = torch.zeros(N+1, device=device)
    CosiBeta = torch.zeros(N+1, device=device)
    for j in range(1, N+1):
        xj,yj = coorX[j],coorY[j]
        xi_star, yi_star = Cosi[j]*(x0-xj)+Sine[j]*(y0-yj), Cosi[j]*(y0-yj)-Sine[j]*(x0-xj)
        l = Leng[j]
        c1 = (xi_star-l)/Rlen[j+1]
        s1 = yi_star/Rlen[j+1]
        c2 = xi_star/Rlen[j]
        s2 = yi_star/Rlen[j]
        SineBeta[j] = s1*c2-s2*c1
        CosiBeta[j] = c1*c2+s1*s2
        if abs(SineBeta[j])<1e-5:
            SineBeta[j] = 0

    Us_star = torch.zeros(N+1,device=device)
    Vs_star = torch.zeros(N+1,device=device)
    Uv_star = torch.zeros(N+1,device=device)
    Vv_star = torch.zeros(N+1,device=device)

    for j in range(1, N+1):
        Us_star[j] = -math.log(Rlen[j+1]/Rlen[j])/(2*math.pi)
        Vs_star[j] = torch.atan2(SineBeta[j], CosiBeta[j])/(2*math.pi)
        if Vs_star[j].isnan():
            print(j)
        if abs(Vs_star[j]+0.5)<1e-4:
            Vs_star[j]=0.5
        Uv_star[j] = Vs_star[j]
        Vv_star[j] = -Us_star[j]

    Us = torch.zeros(N+1,device=device)
    Vs = torch.zeros(N+1,device=device)
    Uv = torch.zeros(N+1,device=device)
    Vv = torch.zeros(N+1,device=device)

    for j in range(1, N+1):
        Us[j] = Us_star[j]*Cosi[j] - Vs_star[j]*Sine[j]
        Vs[j] = Us_star[j]*Sine[j] + Vs_star[j]*Cosi[j]
        Uv[j] = Uv_star[j]*Cosi[j] - Vv_star[j]*Sine[j]
        Vv[j] = Uv_star[j]*Sine[j] + Vv_star[j]*Cosi[j]
    return Us,Uv,Vs,Vv


def strengths_single_edge(ed, foil, device="cpu"):
    Us,Uv,Vs,Vv = strengths_single_point(ed.mid, foil, device=device)
    # T代表切向,N代表法向,s代表源,v代表涡
    Ts,Ns = ed.cosi*Us + ed.sine*Vs, -ed.sine*Us + ed.cosi*Vs
    Tv,Nv = ed.cosi*Uv + ed.sine*Vv, -ed.sine*Uv + ed.cosi*Vv
    return Ts,Ns,Tv,Nv



def strengths_group_edge(edgelist, foil, device="cpu"):
    M=len(edgelist)
    N=foil.Num

    Ts = torch.zeros((M,N+1),device=device)
    Tv = torch.zeros((M,N+1),device=device)
    Ns = torch.zeros((M,N+1),device=device)
    Nv = torch.zeros((M,N+1),device=device)
    for i in range(1,M):
        ed = edgelist[i]
        Ts[i],Ns[i],Tv[i],Nv[i] = \
            strengths_single_edge(ed, foil, device="cpu")
    return Ts,Ns,Tv,Nv