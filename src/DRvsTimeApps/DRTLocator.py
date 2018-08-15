#!/usr/bin/python3
# Author: Ding, Liang
# Email: liangding86@gmail.com
# Date: 2018-01-07

import numpy as np
from DRvsTimeApps.DRTRayTracer import DRTRayTracer as DRTRT

class DRTLocator(object):

    def __init__(self):
        self.drtrt = DRTRT()
        self.m_bInitialize = False
        self.m_bHasLocate = False
        self.m_inPos = np.array([0,0,0])
        self.m_inVec = np.array([0,0,0])
        self.m_numLayers = 0


    def SetParameters(self,inPos, inVec, numLayers, timeLimit):
        self.m_bInitialize = False
        self.m_bHasLocate = False
        self.m_timeLimit = timeLimit
        if (self.m_inPos != inPos).any() or (self.m_inVec != inVec).any() or (self.m_numLayers != numLayers):
            self.m_inPos = inPos
            self.m_inVec = inVec
            self.m_numLayers = numLayers
            self.__Initialize__()


    def __Initialize__(self):
        self.drtrt.SetParameters(inPos=self.m_inPos, inVec=self.m_inVec, numLayers=self.m_numLayers)
        self.drtrt.GoReverse()
        self.m_bInitialize = True


    def GetRayPath(self):
        if False == self.m_bHasLocate:
            self.GoLocator()
        return self.rayPathArr.copy()


    def GoLocator(self):
        midPointsArr = self.drtrt.GetMidPointsArr()
        travelTimeArr = self.drtrt.GetTraveTimeArr()
        timeLmt = self.m_timeLimit
        sumTt = 0
        numMidPoint = midPointsArr.__len__()
        tmpPathArr = np.zeros([numMidPoint + 1, 3])
        pathIdx = 0
        tmpFinalIdx = 0
        bInitialPath = False

        for idx in np.arange(0, numMidPoint):
            if (np.array([0.0, 0.0, 0.0]) == midPointsArr[idx]).all():
                continue

            if False == bInitialPath:
                tmpPathArr[pathIdx] = midPointsArr[idx]
                pathIdx += 1
                bInitialPath = True
                continue

            sumTt = sumTt + travelTimeArr[idx - 1]
            if sumTt < timeLmt:
                tmpPathArr[pathIdx] = midPointsArr[idx]
                pathIdx += 1
            else:
                tmpFinalIdx = idx
                sumTt = sumTt - travelTimeArr[idx - 1]
                break


        if 0 == tmpFinalIdx:
            delTime = timeLmt - sumTt
            delT10 = travelTimeArr[tmpFinalIdx - 1]
            P1 = midPointsArr[tmpFinalIdx - 2]
            P2 = midPointsArr[tmpFinalIdx - 1]
            finalPoint = ((delTime + delT10) / delT10) * (P2 - P1) + P1

        else:
            delTime = timeLmt - sumTt
            delT10 = travelTimeArr[tmpFinalIdx - 1]
            P1 = midPointsArr[tmpFinalIdx - 1]
            P2 = midPointsArr[tmpFinalIdx]
            finalPoint = (delTime / delT10) * (P2 - P1) + P1

        tmpPathArr[pathIdx] = finalPoint

        numCounter = 0
        for idx in np.arange(0, numMidPoint):
            if (np.array([0.0, 0.0, 0.0]) == midPointsArr[idx]).all():
                continue
            numCounter += 1

        self.rayPathArr = np.zeros([pathIdx+1, 3])
        for idx in np.arange(0, pathIdx+1):
            self.rayPathArr[idx] = tmpPathArr[idx]

        self.m_bHasLocate = True


    def DVariance(pointsArr):
        return np.var(pointsArr[:, 0]) + \
               np.var(pointsArr[:, 1]) + \
               np.var(pointsArr[:, 2])


if __name__ == "__main__":
    inPos = np.array([100, 100, 50])
    inVec = np.array([-1, -1, -4])
    Rtime = 0.3
    from DModelMgrApps.DIntfaceVel import DCountLayers
    numLayers = DCountLayers()

    dLocator = DRTLocator()

    dLocator.SetParameters(inPos=inPos, inVec=inVec, numLayers=numLayers, timeLimit=Rtime)
    print("rayPath={}".format(dLocator.GetRayPath()))
