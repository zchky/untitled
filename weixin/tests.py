
from matplotlib import pyplot as plt
import numpy as np
y=list(range(10))

x=list(range(10))
# z=[[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,9],[10,10]]
# k=[[5,5],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,9],[10,10]]
# k=[[[15, 13]], [], [], [], []]
# z=[[20.233333333333334, 16.416666666666668]]

k=[[[1,2,3,4],[5,6,7,8]]]
z=[[1,2,3,4],[1,2,3,4]]
# y=[[1,2],[2,3],[3,4]]
# x=[[1,1],[2,2],[3,3]]
y=np.array(k[0])
y=y.transpose()
x=np.array(z)
x=x.transpose()
print(y.shape)
print(y)
print(x.shape)
print(x)
# print(y)
# print(y.shape)
# print(x.shape)
# z=[x[] for x in z]
# z=map(lambda x :x[1]+1,z)
# z=[x[1]+1]
# z=list(z)
# c=z[:][1]+1

# print(z[:])
plt.plot(x,y)
plt.ylim([0,10])
plt.xlim([0,10])
plt.plot(x,y,'-')
plt.show()
