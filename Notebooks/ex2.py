#%% imports
import numpy as np
import matplotlib.pyplot as plt

#%% functions
def fun(x):
    return x**2
#%% plot
f, ax = plt.subplots(1, 1)
x = np.linspace(-10, 10, 101)
y = fun(x)
ax.plot(x, y)
#%%
