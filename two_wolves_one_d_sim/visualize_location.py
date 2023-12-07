import pandas as pd
import matplotlib.pyplot as plt

simulations = pd.read_csv('two_wolves_one_d_sim/simulated_data/simulations.csv')

idx = 7
file = simulations['Name'][idx]
size = simulations['AreaSize'][idx]

print(file)

data = pd.read_csv(f'two_wolves_one_d_sim/simulated_data/{file}')
plt.hist(data['A'], bins=size, range=(0, size), color='blue', alpha=0.7)
plt.hist(data['B'], bins=size, range=(0, size), color='orange', alpha=0.7)
# plt.hist(data['C'], bins=size, range=(0, size), color='green', alpha=0.7)
plt.show() 
