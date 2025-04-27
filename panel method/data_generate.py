import numpy as np
import random
import math
import airfoil
import landscape
from solverN import solverN_traditional
trainlist = ['0012','2412','4412','5412']
testlist = ['23012','23015']
COORX,COORY = {},{}
for name in trainlist+testlist:
    load_properties=np.load("properties/"+name+"_properties.npz")
    COORX[name] = load_properties["coorX"]
    COORY[name] = load_properties["coorY"]
print("finished reading from properties")
# 生成训练数据
data_size = 2
num_foil = 2
num_points = 100
vertices = np.zeros((data_size,num_foil,num_points,2))
q_true = np.zeros((data_size,num_foil,num_points-1))
gamma_true = np.zeros((data_size,num_foil,1))
for cnt in range(data_size):
    print(cnt)
    foils = [None]
    for k in range(num_foil):
        name = random.choice(trainlist)
        coorX_temp,coorY_temp = COORX[name],COORY[name]
        movementx,movementy = random.uniform(-2,2),random.uniform(-2,2)
        theta = random.uniform(0,2*math.pi)
        coorX,coorY = [None],[None]
        for i in range(num_points):
            x = movementx+math.cos(theta)*coorX_temp[i+1]+\
                math.sin(theta)*coorY_temp[i+1]
            y = movementy-math.sin(theta)*coorX_temp[i+1]+\
                math.cos(theta)*coorY_temp[i+1]
            coorX.append(x)
            coorY.append(y)
            vertices[cnt][k][i][0],vertices[cnt][k][i][1] = x,y
        foils.append(airfoil.listtofoil(coorX,coorY))
    landsc = landscape.landscape(foils)
    q = solverN_traditional(landsc, 0, 1, only_q=True)
    for k in range(num_foil):
        q_true[cnt][k] = q[k+1][1:-1]
        gamma_true[cnt][k][0] = q[k+1][-1]
    print("finished training data no. "+str(cnt))
np.savez("../data/train_data.npz",vertices=vertices,q_true=q_true,gamma_true=gamma_true)
print("saved training data")

# 生成测试数据
data_size = 1
num_foil = 2
num_points = 100
vertices = np.zeros((data_size,num_foil,num_points,2))
q_true = np.zeros((data_size,num_foil,num_points-1))
gamma_true = np.zeros((data_size,num_foil,1))
for cnt in range(data_size):
    foils = [None]
    for k in range(num_foil):
        name = random.choice(testlist)
        coorX_temp,coorY_temp = COORX[name],COORY[name]
        movementx,movementy = random.uniform(-2,2),random.uniform(-2,2)
        theta = random.uniform(0,2*math.pi)
        coorX,coorY = [None],[None]
        for i in range(num_points):
            x = movementx+math.cos(theta)*coorX_temp[i+1]+\
                math.sin(theta)*coorY_temp[i+1]
            y = movementy-math.sin(theta)*coorX_temp[i+1]+\
                math.cos(theta)*coorY_temp[i+1]
            coorX.append(x)
            coorY.append(y)
            vertices[cnt][k][i][0],vertices[cnt][k][i][1] = x,y
        foils.append(airfoil.listtofoil(coorX,coorY))
    landsc = landscape.landscape(foils)
    q = solverN_traditional(landsc, 0, 1, only_q=True)
    for k in range(num_foil):
        q_true[cnt][k] = q[k+1][1:-1]
        gamma_true[cnt][k][0] = q[k+1][-1]
    print("finished testing data no. "+str(cnt))
np.savez("../data/test_data.npz",vertices=vertices,q_true=q_true,gamma_true=gamma_true)
print("saved testing data")