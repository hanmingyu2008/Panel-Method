import geometry
from geometry import point,edge

class airfoil:
    def __init__(self, pointlist):
        if pointlist[0] != None:
            raise ValueError("点列头一项务必为None")
        self.points = pointlist # 这是点列,从1开始数,如果闭合那么最后一项要等于1号,最好按顺时针排列
        self.edges = [None]
        self.Num = len(pointlist)-2 # 这是边数,点的坐标是从1到N+1
        for i in range(1,self.Num+1):
            self.edges.append(edge(pointlist[i],pointlist[i+1]))
        self.control = [None]
        for i in range(1,self.Num+1):
            self.control.append(self.edges[i].mid)
        # self.Leng,self.Sine,self.Cosi = geometry.panels_geometry(self.edges)
        self.Leng,self.Sine,self.Cosi = [None],[None],[None]
        for i in range(1,self.Num+1):
            self.Leng.append(self.edges[i].leng)
            self.Sine.append(self.edges[i].sine)
            self.Cosi.append(self.edges[i].cosi)
    def tolist(self):
        coorX = [None for _ in range(self.Num+2)]
        coorY = [None for _ in range(self.Num+2)]
        for i in range(1,self.Num+2):
            coorX[i],coorY[i] = self.points[i].x,self.points[i].y
        return coorX,coorY

def listtofoil(coorX, coorY):
    #从坐标点列到机翼
    N = len(coorX)-1
    pl = [None]
    if len(coorY)!=N+1:
        raise ValueError("两个坐标列必须长度一样")
    for i in range(1,N+1):
        pl.append(point(coorX[i],coorY[i]))
    return airfoil(pl)