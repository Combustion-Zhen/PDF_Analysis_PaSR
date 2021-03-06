"""
Zhen Lu, 2017/07/12 <albert.lz07@gmail.com>
Plot PaSR results, scatter plot in Z, T space
"""

import numpy as np
import matplotlib.pyplot as plt

SMALL = 1.e-20
# import data
particle = np.genfromtxt('particle_post.dat')

# Temperature

fig = plt.figure(2)

plt.scatter(particle[:,0],particle[:,4])

plt.ylabel('T')

plt.show()

# Progress variable

fig = plt.figure(3)

plt.scatter(particle[:,0],particle[:,1])

plt.ylabel('C')

plt.show()

Z=[]
I=[]
I_S=[]
for p in particle:
    if ( abs(p[-1]) > SMALL or abs(p[-2]) > SMALL ) and p[0] > 1e-4 and p[0] < 1.-1.1e-4 :
    #if ( abs(p[-1]) > SMALL or abs(p[-2]) > SMALL ):
        Z.append(p[0])
        I.append(p[3])
        dC = abs(p[-2])/max(p[1],SMALL)
        dZ = abs(p[-3])/max(p[0],SMALL)
        #NI=abs(p[-1])/(abs(p[-1])+abs(p[-2]))
        NI=dC/(dC+dZ)
        I_S.append(NI)
    else:
        print(p)

fig = plt.figure(4)

plt.scatter(Z,I)
plt.ylabel('I_phi')
plt.show()

print(np.average(np.array(I)))

fig = plt.figure(5)

plt.scatter(Z,I_S)
plt.ylabel('I_Z')
plt.show()

print(np.average(np.array(I_S)))
