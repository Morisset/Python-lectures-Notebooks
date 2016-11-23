import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import pandas as pd
import pymysql

def dens_plot(x, y, ax=None, *args, **kwargs):
    # Calculate the point density and plot it into ax.
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    if ax is None:
        fig, ax = plt.subplots()
    ax.scatter(x, y, c=z, edgecolor='', *args, **kwargs)    

co = pymysql.connect(host='132.248.1.102', db='3MdB', user='OVN_user', passwd='oiii5007')
res = pd.read_sql("""SELECT 
H__1__4861A as Hb,
H__1__6563A as Ha,
O__3__5007A as O3,
N__2__6584A as N21,
TOTL__3727A/H__1__4861A as R2, 
(N__2__6584A+N__2__6548A)/H__1__4861A as N2,
(S_II__6716A+S_II__6731A)/H__1__4861A as S2,
(O__3__5007A+O__3__4959A)/H__1__4861A as R3,
12+OXYGEN as O
FROM tab WHERE ref = 'CALIFA_ah' AND abs(com5) < 0.1 AND com7 > 0.8 AND com6 = 'Neb'
""", con=co)
co.close()

print('Number of models: {}'.format(len(res)))
R2 = res['R2']
N2 = res['N2']
S2 = res['S2']
R3 = res['R3']
O = res['O']
O3N2 = res['O3']/res['Hb'] / (res['N21']/res['Ha'])

# Generic function from Pilyuin 2016
OoH = lambda a, R3, N2, SR2: (a[0] + a[1] * np.log10(R3/SR2) + a[2] * np.log10(N2) +
			      (a[3] + a[4] * np.log10(R3/SR2) + a[5] * np.log10(N2)) * np.log10(SR2))

# R method: defining coefficients
a_u = (8.589, 0.022, 0.399, -0.137, 0.164, 0.589)
a_l = (7.932, 0.944, 0.695, 0.970, -0.291, -0.019)

# Using where to select the upper or lower branch
OoHR = np.where(np.log(N2) > -0.6, OoH(a_u, R3, N2, R2), OoH(a_l, R3, N2, R2))

# S method: defining coefficients
a_u = (8.424, 0.030, 0.751, -0.349, 0.182, 0.508)
a_l = (8.072, 0.789, 0.726, 1.069, -0.170, 0.022)

OoHS = np.where(np.log(N2) > -0.6, OoH(a_u, R3, N2, S2), OoH(a_l, R3, N2, S2))

# Marino O/H
oh_marino = 8.533 - 0.214 * np.log10(O3N2)

# First plot, using alpha to access the density
f1, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2, 2, figsize=(9, 9))
alpha = 0.1
size = 30
for ax in (ax1, ax2, ax3, ax4):
    ax.set_xlim((8,9))
    ax.set_ylim((8,9))
    ax.plot((8,9), (8,9), c='green', alpha=0.9)
ax1.scatter(O, oh_marino, c='blue', edgecolor='None', label='OH Marino', s=size, alpha=alpha)
ax1.set_xlabel('12 + log(O/H) Ori')
ax1.set_ylabel('12 + log(O/H) Marino')
ax2.scatter(OoHR, OoHS, c='blue', edgecolor='None', label='OH S', s=size, alpha=alpha)
ax2.set_xlabel('12 + log(O/H) R')
ax2.set_ylabel('12 + log(O/H) S')
ax3.scatter(O, OoHR, c='blue', edgecolor='None', label='OH R', s=size, alpha=alpha)
ax3.set_xlabel('12 + log(O/H) Ori')
ax3.set_ylabel('12 + log(O/H) R')
ax4.scatter(O, OoHS, c='blue', edgecolor='None', label='OH S', s=size, alpha=alpha)
ax4.set_xlabel('12 + log(O/H) Ori')
ax4.set_ylabel('12 + log(O/H) S')
f1.tight_layout()

# Second plot, using hexbin
f2, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2, 2, figsize=(9, 9))
extent = [8,9,8,9]
gridsize = 40
ax1.hexbin(O, oh_marino,gridsize=gridsize,extent=extent,mincnt=1,bins='log')
ax1.set_xlabel('12 + log(O/H) Ori')
ax1.set_ylabel('12 + log(O/H) Marino')
ax2.hexbin(OoHR, OoHS,gridsize=gridsize,extent=extent,mincnt=1,bins='log')
ax2.set_xlabel('12 + log(O/H) R')
ax2.set_ylabel('12 + log(O/H) S')
ax3.hexbin(O, OoHR,gridsize=gridsize,extent=extent,mincnt=1,bins='log')
ax3.set_xlabel('12 + log(O/H) Ori')
ax3.set_ylabel('12 + log(O/H) R')
ax4.hexbin(O, OoHS,gridsize=gridsize,extent=extent,mincnt=1,bins='log')
ax4.set_xlabel('12 + log(O/H) Ori')
ax4.set_ylabel('12 + log(O/H) S')
for ax in (ax1, ax2, ax3, ax4):
    ax.set_xlim((8,9))
    ax.set_ylim((8,9))
    ax.plot((8,9), (8,9), c='green', alpha=0.9)
f2.tight_layout()

# Third plot, using dens_plot, define above
f3, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2, 2, figsize=(9, 9))
for ax in (ax1, ax2, ax3, ax4):
    ax.set_xlim((8,9))
    ax.set_ylim((8,9))
    ax.plot((8,9), (8,9), c='green', alpha=0.9)
size=40
dens_plot(O, oh_marino, ax1, s=size)
ax1.set_xlabel('12 + log(O/H) Ori')
ax1.set_ylabel('12 + log(O/H) Marino')
dens_plot(OoHR, OoHS, ax2, s=size)
ax2.set_xlabel('12 + log(O/H) R')
ax2.set_ylabel('12 + log(O/H) S')
dens_plot(O, OoHR, ax3, s=size)
ax3.set_xlabel('12 + log(O/H) Ori')
ax3.set_ylabel('12 + log(O/H) R')
dens_plot(O, OoHS, ax4, s=size)
ax4.set_xlabel('12 + log(O/H) Ori')
ax4.set_ylabel('12 + log(O/H) S')
f3.tight_layout()

plt.show()
