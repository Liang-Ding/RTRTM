#!/usr/bin/python3
# Author: Ding, Liang
# Email: liangding86@gmail.com
# Date: 2018-01-05

import numpy as np
from DModelMgrApps import DIntfaceVel as dmodel
from DRayTracerApps import DRefraction as dray

class DRTRayTracer(object):

    def __init__(self):
        self.m_bInitialize = False
        self.m_bCalculated = False
        pass


    def SetParameters(self, inPos, inVec,numLayers):
        self.m_bInitialize = False
        self.m_inPos = inPos
        self.m_inVec = inVec
        self.m_numLayers = numLayers
        self.__Initialize__()


    def __Initialize__(self):
        self.m_MidPointArr = np.zeros([self.m_numLayers + 1, 3])
        self.m_SegmentLengthArr = np.zeros(self.m_numLayers)
        self.m_TravelTimeArr = np.zeros(self.m_numLayers)
        self.m_bInitialize = True
        self.m_bCalculated = False


    def GetMidPointsArr(self):
        if False == self.m_bCalculated and True == self.m_bInitialize:
            self.GoReverse()

        return self.m_MidPointArr


    def GetSegmentLengthArr(self):
        if False == self.m_bCalculated and True == self.m_bInitialize:
            self.GoReverse()

        return self.m_SegmentLengthArr


    def GetTraveTimeArr(self):
        if False == self.m_bCalculated and True == self.m_bInitialize:
            self.GoReverse()

        return self.m_TravelTimeArr


    def GoReverse(self):
        if False == self.m_bInitialize:
            return False

        midPoint = self.m_inPos
        inVec = self.m_inVec
        refractor = dray.DRefraction()
        bInitial = False
        firstLayer = 0

        for layerIdx in np.arange(0, self.m_numLayers):
            if self.m_inPos[2] < dmodel.DGetDepth(self.m_inPos[0], self.m_inPos[1], dmodel.DInterfaces(layerIdx)):
                continue
            firstLayer = layerIdx
            break

        for layerIdx in np.arange(firstLayer, self.m_numLayers):
            if False == bInitial:
                self.m_MidPointArr[layerIdx] = midPoint
                bInitial = True

            midPoint = dmodel.DGetIntersection(stPos=midPoint, rayVec=inVec, intFace=dmodel.DInterfaces(layerIdx))
            self.m_MidPointArr[layerIdx + 1] = midPoint
            v1 = dmodel.DVelocities(layerIdx)
            v2 = dmodel.DVelocities(layerIdx + 1)
            self.m_SegmentLengthArr[layerIdx] = np.linalg.norm(self.m_MidPointArr[layerIdx + 1] - self.m_MidPointArr[layerIdx])
            self.m_TravelTimeArr[layerIdx] = self.m_SegmentLengthArr[layerIdx] / v1
            nmVec = dmodel.DGetNormal(x=midPoint[0], y=midPoint[1], intFace=dmodel.DInterfaces(layerIdx))
            refractor.SetParas(inVec=inVec, nmVec=nmVec, v1=v1, v2=v2)
            outVec = refractor.GetRefractVec()
            inVec = outVec

        self.m_bCalculated = True




if __name__ == "__main__":
    inPos = np.array([200, 100, 50])
    inVec = np.array([-1, -1, -4])
    numLayers = 8

    drtrt = DRTRayTracer()
    drtrt.SetParameters(inPos=inPos, inVec=inVec, numLayers=numLayers)

    print("midPoint={}".format(drtrt.GetMidPointsArr()))
    print("segment={}".format(drtrt.GetSegmentLengthArr()))
    print("travelTime={}".format(drtrt.GetTraveTimeArr()))
