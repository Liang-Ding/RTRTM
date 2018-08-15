
# Author: Ding, Liang
# Email: liangding86@gmail.com

from DModelMgrApps.DModelTypes import *
import numpy as np

def DVelocities_IASP91(num):
    velocity = np.array([5800, 5800, 5800, 5800, 6500, 8040, 8040.6])
    return velocity[num]


def DGetNumInterface_IASP91():
    return 4


def DInterfaces_IASP91(num):

    def intFace0(x, y):
       return -20E3 + 0 * x + 0.0 * y

    def intFace1(x, y):
       return -25E3 + 0 * x + 0.0 * y

    def intFace2(x, y):
        return -34E3 + 0 * x + 0.0 * y

    def intFace3(x, y):
        return -35E3 + 0 * x + 0.0 * y


    if 0 == num:
        return intFace0
    if 1 == num:
        return intFace1
    if 2 == num:
        return intFace2
    if 3 == num:
        return intFace3

########### END OF RTRTM Model ###########
