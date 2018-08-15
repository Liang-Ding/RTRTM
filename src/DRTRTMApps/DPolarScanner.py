
# Author: Ding, Liang
# Email: liangding86@gmail.com

import numpy as np
g_MINIMUM_AMP = 2E-2


def GetVariances(vecArr):
    component = len(vecArr[0])
    varArr = np.zeros([1,component])

    for idx in np.arange(0,component):
        varArr[0, idx] = np.cov(vecArr[:, idx])
    return varArr


def GetMeanVec(vecArr):
    return np.array([np.mean(vecArr[:,0]),
                     np.mean(vecArr[:,1]),
                     np.mean(vecArr[:,2])])


def DScanPolarity(ampArr, wndLens, step):
    lenData = ampArr.__len__()
    normAmpArr = np.zeros_like(ampArr)

    for idx in np.arange(0,lenData):
        if np.fabs(ampArr[idx,0]) < g_MINIMUM_AMP \
                and np.fabs(ampArr[idx,1]) < g_MINIMUM_AMP \
                and np.fabs(ampArr[idx,2])< g_MINIMUM_AMP :
            normAmpArr[idx,:] = 0
            continue

        else:
            var = np.linalg.norm(ampArr[idx, :])
            normAmpArr[idx, :] = ampArr[idx, :] / var

    tmpArr = np.arange(0, lenData - wndLens + 1, step)
    lenVV = tmpArr.__len__()
    VVArr = np.zeros([lenVV, 6])
    idxVVArr = 0

    for idx in np.arange(0, lenData - wndLens + 1, step):
        VVArr[idxVVArr, 0:3] = GetMeanVec(normAmpArr[idx:idx + wndLens, :])
        VVArr[idxVVArr, 3:6] = GetVariances(normAmpArr[idx:idx + wndLens, :])
        idxVVArr += 1

    return VVArr.copy()



if __name__ == '__main__':
    ampArr = np.random.random_sample([30, 3])
    wndLens = 5
    step = 3
    VVArr = DScanPolarity(ampArr=ampArr, wndLens=wndLens, step=step)

    import matplotlib.pyplot as plt
    plt.figure(1)
    plt.subplot(121)
    plt.plot(VVArr[:,0],'r-', VVArr[:,1],'k^-', VVArr[:,2],'bD-.')
    plt.title('Mean vector')

    plt.subplot(122)
    variance = np.sqrt(np.power(VVArr[:, 3], 2) + np.power(VVArr[:, 4], 2) + np.power(VVArr[:, 5], 2))
    plt.plot(variance)
    plt.title('average deviation')

    plt.show()
