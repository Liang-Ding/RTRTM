#!/usr/bin/python3
# Author: Ding, Liang
# Email: liangding86@gmail.com
# Date: 2017-12-21


import numpy as np

class DReflectionTracer(object):

    def __init__(self, inVec, nmVec, v1, v2):
        self.m_inVec = inVec
        self.m_nmVec = nmVec
        self.m_v1 = v1
        self.m_v2 = v2
        self.m_outVec = np.zeros(3)
        self.m_bHasCalculate = False


    def __CheckData__(self):
        if type(np.ndarray(3)) != type(self.m_inVec):
            print("Incident vector should be numpy array!!!")
            return False

        if type(np.ndarray(3)) != type(self.m_nmVec):
            print("Normal vector should be numpy array!!!")
            return False

        if self.m_v1 == self.m_v2:
            print("Check Velocity Structure!!!")
            return False

        return True


    def SetIncidentVec(self,inVec):
        self.m_inVec = inVec
        self.m_bHasCalculate = False


    def SetNormalVec(self,nmVec):
        self.m_nmVec = nmVec
        self.m_bHasCalculate = False


    def SetVelocity(self, v1, v2):
        self.m_v1 = v1
        self.m_v2 = v2


    def __CalculateReflectVec__(self):
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

        p1= 2.0*inVec[0]*nVec[0]+2.0*inVec[1]*nVec[1]+\
            inVec[2] *(np.power(nVec[0], 2) + np.power(nVec[1], 2) -1.0)
        p2 = np.sum(np.power(nVec, 2))

        outVec = np.array([1.0, 1.0, 1.0])
        outVec[2] = p1/p2
        outVec[1] = inVec[1] + inVec[2] * nVec[1] - outVec[2] * nVec[1]
        outVec[0] = inVec[0] + inVec[2] * nVec[0] - outVec[2] * nVec[0]

        if True == bReverse:
            outVec = outVec * -1

        self.m_outVec = outVec / np.linalg.norm(outVec)
        self.m_bHasCalculate = True


    def GetReflectVec(self):
        if False == self.m_bHasCalculate:
            self.__CalculateReflectVec__()

        return self.m_outVec


if __name__ == "__main__":
    inVec = np.array([1,1,1])
    nmVec = np.array([0,0,-1])
    v1 = 3500
    v2 = 3600

    reflTrcer = DReflectionTracer(inVec, nmVec, v1, v2)
    outVec = reflTrcer.GetReflectVec()
    print("Reflect vector={}".format(outVec))
