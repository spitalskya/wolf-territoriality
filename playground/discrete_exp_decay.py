import numpy as np
import matplotlib.pyplot as plt


x = [1]
for i in range(1, 30):
    if i % 9 == 0:
        x.append(x[i - 1] + 1)
        continue
    x.append(x[i - 1]*(np.e**(-0.5)))

exp_x = [x for x in range(20)]
exp_y = [np.e**(-0.5*x) for x in exp_x]

plt.plot(x, 'o')
plt.plot(exp_x, exp_y)
plt.show()