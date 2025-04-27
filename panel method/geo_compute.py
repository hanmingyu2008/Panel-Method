# 以后我们使用这个程序进行panel method中几何部分的运算
import numpy as np
import torch 
import math
# 注意，对于几何描述的数组，我们从来都把第0项设为0，从第1项开始记录有效数据
# 另外，coorX和coorY从来都要首尾链接。即大小为N+2,N为点的个数。

def panels_geometry(coorX, coorY, device="cpu"):
    N = len(coorX)-2
    if len(coorY)!=N+2:
        raise ValueError("两个坐标元素个数务必相等!")
    mid_points = torch.zeros((N+1,3),device=device)
    for i in range(1, N+1):
        mid_points[i][1] = 0.5*(coorX[i]+coorX[i+1])
        mid_points[i][2] = 0.5*(coorY[i]+coorY[i+1])
    Sine = torch.zeros(N+2,device=device) #sin\theta_i
    Cosi = torch.zeros(N+2,device=device)  #cos\theta_i
    Leng = torch.zeros(N+2,device=device)  #l_i(panel长度)

    for i in range(1, N+1):
        Leng[i] = math.sqrt((coorX[i]-coorX[i+1])**2+(coorY[i]-coorY[i+1])**2)
        Sine[i] = (coorY[i+1]-coorY[i])/Leng[i]
        Cosi[i] = (coorX[i+1]-coorX[i])/Leng[i]
    Leng[N+1],Sine[N+1],Cosi[N+1] = Leng[1],Sine[1],Cosi[1]

    return mid_points,Leng,Sine,Cosi

def panels_geometry_withgap(coorX, coorY, device="cpu"):
    #这个是针对于尾翼略去一条panel，形成一个间隙的数据类型
    #当然,这里的coorX和coorY不可以首位相连 共N+1个顶点,N个Panel
    N = len(coorX)-2
    if len(coorY)!=N+2:
        raise ValueError("两个坐标元素个数务必相等!")
    mid_points = torch.zeros((N+1,3),device=device)
    for i in range(1, N+1):
        mid_points[i][1] = 0.5*(coorX[i]+coorX[i+1])
        mid_points[i][2] = 0.5*(coorY[i]+coorY[i+1])
    Sine = torch.zeros(N+1,device=device) #sin\theta_i
    Cosi = torch.zeros(N+1,device=device)  #cos\theta_i
    Leng = torch.zeros(N+1,device=device)  #l_i(panel长度)

    for i in range(1, N+1):
        Leng[i] = math.sqrt((coorX[i]-coorX[i+1])**2+(coorY[i]-coorY[i+1])**2)
        Sine[i] = (coorY[i+1]-coorY[i])/Leng[i]
        Cosi[i] = (coorX[i+1]-coorX[i])/Leng[i]

    return mid_points,Leng,Sine,Cosi

def strengths_single(x0,y0, coorX, coorY, Leng, Sine, Cosi, device="cpu"):
    N = len(coorX)-2
    Rlen = torch.zeros(N+2, device=device)
    for j in range(1, N+1):
        Rlen[j] = math.sqrt((x0-coorX[j])**2+(y0-coorY[j])**2)
    Rlen[N+1] = Rlen[1]
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

def strengths_single_withgap(x0,y0, coorX, coorY, Leng, Sine, Cosi, device="cpu"):
    N = len(coorX)-2
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

def strengths_group(listx,listy, coorX, coorY, Leng, Sine, Cosi, device="cpu"):
    M = len(listx)
    N = len(coorX)-2
    if len(listy)!=M:
        raise ValueError("len(listx)=len(listy) 必须成立")
    Us = torch.zeros((M,N+1),device=device)
    Uv = torch.zeros((M,N+1),device=device)
    Vs = torch.zeros((M,N+1),device=device)
    Vv = torch.zeros((M,N+1),device=device)
    for i in range(1,M):
        x0,y0 = listx[i],listy[i]
        Us[i],Uv[i],Vs[i],Vv[i] = \
        strengths_single(x0,y0, coorX, coorY, Leng, Sine, Cosi, device="cpu")
    return Us,Uv,Vs,Vv

def strengths_group_withgap(listx,listy, coorX, coorY, Leng, Sine, Cosi, device="cpu"):
    M = len(listx)
    N = len(coorX)-2
    if len(listy)!=M:
        raise ValueError("len(listx)=len(listy) 必须成立")
    Us = torch.zeros((M,N+1),device=device)
    Uv = torch.zeros((M,N+1),device=device)
    Vs = torch.zeros((M,N+1),device=device)
    Vv = torch.zeros((M,N+1),device=device)
    for i in range(1,M):
        x0,y0 = listx[i],listy[i]
        Us[i],Uv[i],Vs[i],Vv[i] = \
        strengths_single_withgap(x0,y0, coorX, coorY, Leng, Sine, Cosi, device="cpu")
    return Us,Uv,Vs,Vv