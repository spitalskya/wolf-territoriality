import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('two_wolves_one_d_sim/loc_end.csv')
plt.hist(data['A'], bins=40, range=(0, 40), color='blue')
plt.hist(data['B'], bins=40, range=(0, 40), color='orange')
plt.show() 
# data['B'].plot.hist()
