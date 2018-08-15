
# Author: Ding, Liang
# Email: liangding86@gmail.com

from DModelMgrApps.DModelTypes import *
import numpy as np


def DVelocities_RTRTM(num):
    velocity = np.array([3200, 3250, 3300, 3350, 3400, 3450, 3500, 3550, 3600])
    return velocity[num]

def DGetNumInterface_RTRTM():
    return 8


def DInterfaces_RTRTM(num):

    def intFace0(x, y):
        if g_InterfaceType == 'Panel':
            return 100 + 0 * x + 0.0 * y
        else:
            return 100.0 + 10.0 * (np.sin(0.0005*x) + np.cos(0.0001*y))


    def intFace1(x, y):
        if g_InterfaceType == 'Panel':
            return -200 + 0 * x + 0.0 * y
        else:
            return -200.0 + 10.0 * (np.sin(0.0001*x)+ np.cos(0.0004*y))


    def intFace2(x, y):
        if g_InterfaceType == 'Panel':
            return -500 + 0 * x + 0.0 * y
        else:
            return -500.0 + 10.0 * (np.sin(0.0001*x)+ np.cos(0.0003*y))


    def intFace3(x, y):
        if g_InterfaceType == 'Panel':
            return -800 + 0 * x + 0.0 * y
        else:
            return -800.0 + 10.0 * (np.cos(0.0003*x)+ np.cos(0.0001*y))


    def intFace4(x, y):
        if g_InterfaceType == 'Panel':
            return -1100 + 0 * x + 0.0 * y
        else:
            return -1100.0 + 10.0 * (np.sin(0.0001*x)+ np.cos(0.0005*y))


    def intFace5(x, y):
        if g_InterfaceType == 'Panel':
            return -1400 + 0 * x + 0.0 * y
        else:
            return -1400.0 + 10.0 * (np.sin(0.0003*x)+ np.cos(0.0001*y))


    def intFace6(x, y):
        if g_InterfaceType == 'Panel':
            return -1700 + 0 * x + 0.0 * y
        else:
            return -1700.0 + 10.0 * (np.sin(0.0001*x)+ np.cos(0.0005*y))


    def intFace7(x, y):
        if g_InterfaceType == 'Panel':
            return -2000 + 0 * x + 0.0 * y
        else:
            return -2000.0 + 10.0 * (np.sin(0.0001*x)+ np.cos(0.0005*y))


    if 0 == num:
        return intFace0
    if 1 == num:
        return intFace1
    if 2 == num:
        return intFace2
    if 3 == num:
        return intFace3
    if 4 == num:
        return intFace4
    if 5 == num:
        return intFace5
    if 6 == num:
        return intFace6
    if 7 == num:
        return intFace7

########### END OF RTRTM Model ###########
