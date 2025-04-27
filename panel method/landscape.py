class landscape:
    def __init__(self, foillist):
        self.foils = foillist
        self.size = len(foillist)-1
        self.Numlist = [None]
        for i in range(1,self.size+1):
            self.Numlist.append(self.foils[i].Num)
        # 下面这个用于组成矩阵
        self.templist = [None,0]
        for i in range(2,self.size+1):
            self.templist.append(self.templist[i-1]+self.foils[i-1].Num+1)
        self.totlength = self.templist[-1]+self.foils[-1].Num+1  #这是矩阵的总长度