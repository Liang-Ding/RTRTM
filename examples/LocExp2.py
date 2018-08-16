
# example
# Author: Ding, Liang
# Email: liangding86@gmail.com

import numpy as np
from DRTRTMApps.DLocate import DLocate_RTRTM
import matplotlib.pyplot as plt

dataPath = 'polar2Locate.csv'
timeSta = 0.1
timeEnd = 1.5
dt = 0.05

locator = DLocate_RTRTM(dataPath=dataPath, timeSta=timeSta,
                        timeEnd=timeEnd, dt=dt)
timeVar = locator.GetTimeVariance()
srcPos = locator.GetSource()
rayPathArr = locator.GetReversedRayPath()

print('src location=', srcPos)

plt.figure(1)
plt.plot(timeVar[:, 0], timeVar[:, 1])

from DRTRTMApps.DDataIO import DReadCSV
from mpl_toolkits.mplot3d import Axes3D
datArr = DReadCSV(filePath=dataPath)
recPos = datArr[:, 0:3]
nReciver = recPos.__len__()
fig = plt.figure(2)
for each_Station in np.arange(0, nReciver):
    ax = fig.gca(projection='3d')
    ax.plot(rayPathArr[:, each_Station, :][:, 0],
            rayPathArr[:, each_Station, :][:, 1],
            rayPathArr[:, each_Station, :][:, 2])


plt.show()

