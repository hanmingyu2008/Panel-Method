import numpy as np
data=np.load("data/5412_data.npz")
q=data["Cp"]
gamma = data["Gamma"]
with open("cp.dat","w") as file:
    for i in range(1,len(q)):
        print(q[i],file=file)