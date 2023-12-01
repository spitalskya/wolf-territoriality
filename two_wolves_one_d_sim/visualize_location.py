import pandas as pd
import matplotlib.pyplot as plt

simulations = pd.read_csv('two_wolves_one_d_sim/simulated_data/simulations.csv')

file = simulations['Name'][0]
data = pd.read_csv(f'two_wolves_one_d_sim/simulated_data/{file}')
plt.hist(data['A'], bins=30, range=(0, 30), color='blue', alpha=0.7)
plt.hist(data['B'], bins=30, range=(0, 30), color='orange', alpha=0.7)
plt.show() 
