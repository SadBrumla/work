import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,100)

p1 = np.array([2,1,2,5])
p2 = np.array([1,1.2, 3 , -1])
p3 = np.array([-1,0.8, -1 , 2])

p4 = p1 + p2 - p3

y1 = np.polyval(p1,x)
y2 = np.polyval(p2,x)
y3 = np.polyval(p3,x)
y4 = np.polyval(p4,x)

plt.scatter(x,y1)
plt.scatter(x,y2)
plt.scatter(x,y3)
plt.scatter(x,y4)
plt.legend()
plt.show()