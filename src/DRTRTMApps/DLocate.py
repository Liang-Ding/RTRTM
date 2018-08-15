
# Author: Ding, Liang
# Email: liangding86@gmail.com

import numpy as np
from DModelMgrApps.DIntfaceVel import DCountLayers
from DRvsTimeApps.DRTSrcLocator import DRTSrcLocator
from DRTRTMApps.DDataIO import DReadCSV


def DLocate_RTRTM(dataPath, timeSta, timeEnd, dt):

    datArr = DReadCSV(filePath=dataPath)
    recPos = datArr[:, 0:3]
    tt = datArr[:, 3]
    inVec = datArr[:, 4:7]
    ttMin = tt.min()
    fbTime = tt - ttMin

    numLayers = DCountLayers()

    locator = DRTSrcLocator()
    locator.SetParas(recPosArr=recPos,
                     inVecArr=inVec,
                     fbTimeArr=fbTime,
                     startTime=timeSta,
                     endTime=timeEnd,
                     dt=dt,
                     numLayer=numLayers)

    locator.SetSavePath()

    return locator
