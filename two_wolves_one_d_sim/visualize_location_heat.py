import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# does this show what i need?

simulations = pd.read_csv('two_wolves_one_d_sim/simulated_data/simulations.csv')

file = simulations['Name'][0]
# data = pd.read_csv(f'two_wolves_one_d_sim/simulated_data/{file}')
data =  pd.read_csv(f'two_wolves_one_d_sim/loc_end_murray_lewis_size_40.csv')
heatmap, xedges, yedges = np.histogram2d(data['A'], data['B'], bins=(40, 40))
extent = [0, 40, 0, 40]

plt.imshow(heatmap.T, extent=extent, origin='lower', cmap='viridis_r')
#nonzero_indices = np.nonzero(heatmap)
#plt.scatter(xedges[nonzero_indices[0]], yedges[nonzero_indices[1]], color='red', marker='s', s=50)

plt.show() 
