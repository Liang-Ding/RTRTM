
# Author: Ding, Liang
# Email: liangding86@gmail.com


from DModelMgrApps.MD_IASP91 import *
from DModelMgrApps.MD_RTRTM import *
from scipy import optimize
import numpy as np


def DVelocities(num):
    if "IASP91" == g_ModelType:
        return DVelocities_IASP91(num=num)

    elif "RTRTM" == g_ModelType:
        return DVelocities_RTRTM(num=num)


def DInterfaces(num):
    if "IASP91" == g_ModelType :
        return DInterfaces_IASP91(num=num)

    elif "RTRTM" == g_ModelType:
        return DInterfaces_RTRTM(num=num)


def DCountLayers():
    if "IASP91" == g_ModelType:
        return DGetNumInterface_IASP91()

    elif "RTRTM" == g_ModelType:
        return DGetNumInterface_RTRTM()


def DGetDepth(x, y, intFace):
    return intFace(x,y)


def DGetNormal(x, y, intFace):
    xSpacing = g_xSpacing
    ySpacing = g_ySpacing
    x0 = x-xSpacing
    x1 = x+xSpacing
    y0 = y-ySpacing
    y1 = y+ySpacing
    zx = (DGetDepth(x1, y, intFace=intFace) - DGetDepth(x0, y, intFace=intFace))/2.0
    zy = (DGetDepth(x, y1, intFace=intFace) - DGetDepth(x, y0, intFace=intFace))/2.0

    coeff = np.array([[xSpacing, 0], [0, ySpacing]])
    coeffInv = np.linalg.inv(coeff)
    [[nx], [ny]] = np.dot(coeffInv, np.array([[-1.0 * zx], [-1.0 * zy]]))

    return np.array([nx,ny,1.0])


def DGetDfDx(x, y, intFace):
    xSpacing = g_xSpacing
    x0 = x-xSpacing
    x1 = x+xSpacing
    return (DGetDepth(x1, y, intFace=intFace) - DGetDepth(x0, y, intFace=intFace))/(2.0 * xSpacing)


def DGetDfDy(x, y, intFace):
    ySpacing = g_ySpacing
    y0 = y-ySpacing
    y1 = y+ySpacing
    return (DGetDepth(x,y1,intFace=intFace) - DGetDepth(x,y0,intFace=intFace))/(2.0 * ySpacing)


def DGetDDfDDy(x, y, intFace):
    ySpacing = g_ySpacing
    y0 = y - ySpacing
    y1 = y + ySpacing
    return (DGetDepth(x, y1, intFace=intFace)+DGetDepth(x, y0, intFace=intFace)-2.0 * DGetDepth(x, y,intFace=intFace))/ np.power(ySpacing,2)


def DGetDDfDDx(x, y, intFace):
    xSpacing = g_xSpacing
    x0 = x - xSpacing
    x1 = x + xSpacing
    return (DGetDepth(x0, y, intFace=intFace)+DGetDepth(x1, y, intFace=intFace)-2.0 * DGetDepth(x, y,intFace=intFace))/ np.power(xSpacing,2)



def DGetIntersection(stPos, rayVec, intFace):
    def DRootFinding(t):
        return intFace((stPos[0] + rayVec[0] * t), (stPos[1] + rayVec[1] * t)) - ((stPos[2] + rayVec[2] * t))

    x0 = np.array([0.0])
    res = optimize.fsolve(DRootFinding, x0=x0)
    intersect = np.array([(stPos[0] + rayVec[0] * res[0]),(stPos[1] + rayVec[1] * res[0]),(stPos[2] + rayVec[2] * res[0])])

    return intersect


if __name__ == "__main__":
    x=45
    y=30
    print("Start:")
    print("Depth={}".format(DGetDepth(x=x,y=y,intFace=DInterfaces(0))))
    print("Normal={}".format(DGetNormal(x=x,y=y,intFace=DInterfaces(1))))

    stPos = np.array([40, 45, 50])
    rayVec = np.array([-1, -1, -1])
    print("t={}".format(DGetIntersection(stPos=stPos,rayVec=rayVec,intFace=DInterfaces(1))))
