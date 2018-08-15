
# example
# Author: Ding, Liang
# Email: liangding86@gmail.com


import numpy as np
import matplotlib.pyplot as plt
from obspy import UTCDateTime
from DRTRTMApps.DDenosing import DDenosing_wavelet
from DRTRTMApps.DPolarScanner import DScanPolarity

gSampleRate = 100.0
gDt = 1.0/gSampleRate
wvName = "db2"
wvLevel = 1
wndLens = 4
step = 1

datListDict = {"E": "E.txt",
               "N": "N.txt",
               "Z": "Z.txt"}

tmpData = np.loadtxt(datListDict["Z"])
datLens = tmpData.__len__()
Data = np.zeros([datLens, 3])
Data[:, 0] = tmpData
Data[:, 1] = np.loadtxt(datListDict["N"])
Data[:, 2] = np.loadtxt(datListDict["E"])
PPhase = [7443, 7463]
ScanRange = [7448, 7460]
TimeOK = 7455

StartTime = UTCDateTime("20090101101010")
countPolarity = (ScanRange[1]-ScanRange[0])/step
TimeAxis = np.linspace(ScanRange[0], ScanRange[1], countPolarity+1)

DeNoiseData = np.zeros_like(Data)
for idx in np.arange(0, 3):
    DeNoiseData[:, idx] = DDenosing_wavelet(x=Data[:,idx],
                                              wavelet=wvName,
                                              level=wvLevel)

VecVarArr = DScanPolarity(ampArr=DeNoiseData[(ScanRange[0]-(wndLens-int(wndLens/2))):(ScanRange[1]+int(wndLens/2)),:], wndLens=wndLens, step=step)

plt.figure(1, figsize=(10, 5))
plt.subplot(121)
lensVV = len(VecVarArr)
plt.plot(TimeAxis[:lensVV], VecVarArr[:, 0], 'r-', linewidth=2, label='Z')
plt.plot(TimeAxis[:lensVV], VecVarArr[:, 1], 'k^-',linewidth=2, label='N')
plt.plot(TimeAxis[:lensVV], VecVarArr[:, 2], 'bs-.',linewidth=2, label='E')

VecZ = VecVarArr[TimeOK-ScanRange[0], 0]
VecN = VecVarArr[TimeOK-ScanRange[0], 1]
VecE = VecVarArr[TimeOK-ScanRange[0], 2]
plt.text(TimeOK+0.2, VecZ-0.2, str(VecZ)[:6], color='r')
plt.text(TimeOK+0.2, VecN-0.3, str(VecN)[:5], color='k')
plt.text(TimeOK+0.2, VecE-0.2, str(VecE)[:5], color='b')

plt.ylim([-1.0, 1.0])
plt.legend(loc=3)
plt.vlines(TimeOK, -1.2, 1.2, colors='y', linestyles= 'dashed',linewidth=2)
xAxis = np.linspace(ScanRange[0], ScanRange[1], 4)
xLabel = []
for each_x in xAxis:
    tmpTime = StartTime + (each_x-PPhase[0]) * gDt
    xLabel.append(str("0")+str(tmpTime.time.strftime('%H:%M:%S.%f'))[8:-3])

plt.xticks(xAxis, xLabel)
plt.xlim(ScanRange)
plt.xlabel(str("+")+str((StartTime + PPhase[0] * gDt).time)[:11])
plt.title('Mean vector')


plt.subplot(122)
variance = np.sqrt(np.power(VecVarArr[:, 3], 2) + np.power(VecVarArr[:, 4], 2) + np.power(VecVarArr[:, 5], 2))
plt.vlines(TimeOK, -1.2, 1.2, colors='y', linestyles= 'dashed',linewidth=2)

plt.plot(TimeAxis[:lensVV], variance, linewidth=2, color='k')
plt.title('Standard deviation of vector')
plt.xticks(xAxis, xLabel)
plt.xlim(ScanRange)
plt.ylim([0, 0.1])
plt.xlabel(str("+")+str((StartTime + PPhase[0] * gDt).time)[:11])

plt.show()

