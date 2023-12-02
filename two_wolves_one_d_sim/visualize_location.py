import pandas as pd
import matplotlib.pyplot as plt

simulations = pd.read_csv('two_wolves_one_d_sim/simulated_data/simulations.csv')

file = simulations['Name'][0]
# data = pd.read_csv(f'two_wolves_one_d_sim/simulated_data/{file}')
data =  pd.read_csv(f'two_wolves_one_d_sim/loc_end_murray_lewis_size_40.csv')
plt.hist(data['A'], bins=40, range=(0, 40), color='blue', alpha=0.7)
plt.hist(data['B'], bins=40, range=(0, 40), color='orange', alpha=0.7)
plt.show() 
