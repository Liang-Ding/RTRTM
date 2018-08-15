#!/usr/bin/python3
# Author: Ding, Liang
# Email: liangding86@gmail.com
# Date: 2017-12-21


import numpy as np


class DRefraction(object):

    def __init__(self):
        self.m_outVec = np.zeros(3)
        self.m_bHasCalculate = False

    def __CheckData__(self):
        if type(np.ndarray(3)) != type(self.m_inVec):
            print("Incident vector should be numpy array!!!")
            return False

        if type(np.ndarray(3)) != type(self.m_nmVec):
            print("Normal vector should be numpy array!!!")
            return False

        if 0 > self.m_v1:
            return False

        if 0 > self.m_v2:
            return False

        return True


    def SetParas(self, inVec, nmVec, v1, v2):
        self.m_inVec = inVec
        self.m_nmVec = nmVec
        self.m_v1 = v1
        self.m_v2 = v2
        self.m_outVec = np.zeros(3)
        self.m_bHasCalculate = False


    def SetIncidentVec(self,inVec):
        self.m_inVec = inVec
        self.m_bHasCalculate = False


    def SetNormalVec(self,nmVec):
        self.m_nmVec = nmVec
        self.m_bHasCalculate = False


    def SetV1(self,v1):
        self.m_v1 = v1
        self.m_bHasCalculate = False


    def SetV2(self,v2):
        self.m_v2 = v2
        self.m_bHasCalculate = False


    def __CalculateRefractVec__(self):
        if (False == self.__CheckData__()):
            return False

        if self.m_inVec[2] < 0:
            tmpInVec = self.m_inVec
            bReverse = False
        else:
            tmpInVec = -1 * self.m_inVec
            bReverse = True

        inVec = tmpInVec / np.linalg.norm(tmpInVec)
        nVec  = self.m_nmVec / self.m_nmVec[2] * -1
        lInVec = np.sqrt(self.m_inVec.dot(self.m_inVec))
        lnVec = np.sqrt(self.m_nmVec.dot(self.m_nmVec))
        cosAngle = self.m_inVec.dot(self.m_nmVec)/(lInVec*lnVec)
        v2v1 = self.m_v2 / self.m_v1

        if v2v1 * np.sqrt(1 - (np.power(cosAngle, 2))) > 1:
            print("Critical angle!")
            return False

        p1 = inVec[0] * nVec[0] + inVec[1] * nVec[1] + \
             inVec[2] * (np.power(nVec[0], 2) + np.power(nVec[1], 2))
        p2 = np.sum(np.power(nVec, 2))
        p31 = np.power(inVec[1] * nVec[0] - inVec[0] * nVec[1], 2)
        p32 = np.power(inVec[2] * nVec[0] + inVec[0], 2)
        p33 = np.power(inVec[2] * nVec[1] + inVec[1], 2)
        P = np.sqrt(p2 - np.power(v2v1, 2)*(p31+p32+p33))

        outVec = np.array([1.0,1.0,1.0])
        outVec[2] = v2v1 * p1 - P
        outVec[1] = v2v1*(inVec[1]+inVec[2]*nVec[1])- nVec[1]*outVec[2]
        outVec[0] = v2v1*(inVec[0]+inVec[2]*nVec[0]) - nVec[0]*outVec[2]

        if True == bReverse:
            outVec = outVec * -1

        self.m_outVec = outVec / np.linalg.norm(outVec)
        self.m_bHasCalculate = True


    def GetRefractVec(self):
        if False == self.m_bHasCalculate:
            self.__CalculateRefractVec__()

        return self.m_outVec


if __name__ == "__main__":
    inVec = np.array([-0.5, 0.5, 1.0])
    nmVec = np.array([0, 0, 1])
    v1=1200
    v2=1200
    refrTracer = DRefraction()
    refrTracer.SetParas(inVec, nmVec, v1, v2)
    outVec = refrTracer.GetRefractVec()
    print("Refract vector={}".format(outVec))
