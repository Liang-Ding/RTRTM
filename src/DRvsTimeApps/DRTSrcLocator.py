
# Author: Ding, Liang
# Email: liangding86@gmail.com


import numpy as np
from DRvsTimeApps.DRTLocator import DRTLocator

class DRTSrcLocator(object):

    def __init__(self):
        self.m_SourcePos = np.array([0.0, 0.0, 0.0])
        self.m_bHasSetPara = False
        self.m_bHasLocated = False
        self.m_bStorePath = False
        self.m_minVariance = 9999999999.0


    def __DVariance__(self, endPoints):
        return np.sqrt(np.var(endPoints[:, 0]) +\
                       np.var(endPoints[:, 1]) + \
                       np.var(endPoints[:, 2]))

    def __ComputeSource__(self, endPoints):
        return np.array([np.mean(endPoints[:,0]),
                         np.mean(endPoints[:,1]),
                         np.mean(endPoints[:,2])]).copy()


    def DStatusVariance(self, dt, idx):
        dLocator = DRTLocator()

        for each_rec in np.arange(0,self.m_numRec):
            dLocator.SetParameters(inPos=self.m_recPosArr[each_rec,:],
                                   inVec=self.m_inVecArr[each_rec,:],
                                   numLayers=self.m_numLayers,
                                   timeLimit= self.m_fbTimeArr[each_rec] + dt)

            rayPath = dLocator.GetRayPath()
            self.m_endPoints[each_rec] = rayPath[-1]

        variance = self.__DVariance__(self.m_endPoints)

        if variance < self.m_minVariance:
            self.m_minVariance = variance
            self.m_SourcePos = self.__ComputeSource__(self.m_endPoints)

        if True == self.m_bStorePath:
            self.m_endPointsArr[idx,:,:] = self.m_endPoints.copy()

        return variance.copy()


    def SetSavePath(self):
        self.m_bStorePath = True


    def SetUnSavePath(self):
        self.m_bStorePath = False


    def SetParas(self, recPosArr, inVecArr,fbTimeArr,
                      startTime, endTime,dt, numLayer):

        self.m_bHasLocated = False
        self.m_recPosArr = recPosArr
        self.m_inVecArr = inVecArr
        self.m_fbTimeArr = fbTimeArr
        self.m_startTime = startTime
        self.m_endTime = endTime
        self.m_dt = dt
        self.m_numLayers = numLayer
        self.m_minVariance = 9999999999.0
        self.m_numRec = self.m_recPosArr.__len__()
        self.m_endPoints = np.zeros([self.m_numRec,3])

        if self.m_numRec > self.m_inVecArr.__len__():
            exit()
        elif self.m_numRec > self.m_fbTimeArr.__len__():
            exit()

        self.m_bHasSetPara = True


    def GoLocate(self):
        if False == self.m_bHasSetPara:
            return False

        timeArr = np.arange(self.m_startTime, self.m_endTime+self.m_dt, self.m_dt)
        numTime = timeArr.__len__()

        self.m_timeVarianceArr = np.zeros([numTime, 2])
        self.m_timeVarianceArr[:, 0] = timeArr.copy()

        if True == self.m_bStorePath:
            self.m_endPointsArr = np.zeros([numTime, self.m_numRec, 3])

        for idx in np.arange(0, numTime):
            variance = self.DStatusVariance(dt=timeArr[idx], idx=idx)

            self.m_timeVarianceArr[idx,1] = variance

        self.m_bHasLocated = True


    def GetTimeVariance(self):
        if False == self.m_bHasLocated:
            self.GoLocate()

        return self.m_timeVarianceArr.copy()


    def GetSource(self):
        if False == self.m_bHasLocated:
            self.GoLocate()

        return self.m_SourcePos.copy()


    def GetSourceArray(self):
        if False == self.m_bStorePath:
            return None

        numTime = self.m_timeVarianceArr[:,0].__len__()
        self.m_SourcePosArr = np.zeros([numTime, 3])

        for each_time in np.arange(0,numTime):
            self.m_SourcePosArr[each_time, 0] = np.mean(self.m_endPointsArr[each_time, :, 0])
            self.m_SourcePosArr[each_time, 1] = np.mean(self.m_endPointsArr[each_time, :, 1])
            self.m_SourcePosArr[each_time, 2] = np.mean(self.m_endPointsArr[each_time, :, 2])

        return self.m_SourcePosArr


    def GetReversedRayPath(self):
        if False == self.m_bStorePath:
            return None

        if False == self.m_bHasLocated:
            self.GoLocate()

        return self.m_endPointsArr




if __name__ == '__main__':
    recPos = np.array([[1000.0, 1000.0, 500.0],
                       [1000.0, 500.0, 500.0],
                       [1000.0, 0.0, 500.0],
                       [1000.0, -500.0, 500.0],
                       [1000.0, -1000.0, 500.0]])

    inVec = np.array([[-0.52753853, -0.52835139, -0.66524275],
                       [-0.56301804, -0.42300857, -0.709982],
                       [-0.59325357, -0.29728923, -0.7481105],
                       [-0.61392945, -0.15403676, -0.77418558],
                       [-0.62134420, -4.26876e-04, -0.7835376]])

    fbTime = np.array([0.19859878,
                       0.11513646,
                       0.05241949,
                       0.01334415,
                       0.0        ])

    numLayers = 5

    timeSta = 0.01
    timeEnd = 2.00
    dt = 0.01

    locator = DRTSrcLocator()
    locator.SetParas(recPosArr=recPos,
                 inVecArr=inVec,
                 fbTimeArr=fbTime,
                 startTime=timeSta,
                 endTime=timeEnd,
                 dt=dt,
                 numLayer=numLayers)

    timeVar = locator.GetTimeVariance()
    srcPos = locator.GetSource()

    print('src={}'.format(srcPos))

    import matplotlib.pyplot as plt
    plt.plot(timeVar[:,0],timeVar[:,1])
    plt.show()
