
import pywt
import numpy as np
# import seaborn
from statsmodels.robust import mad


def DDenosing_wavelet(x, wavelet="db4", level=1):

    coeff = pywt.wavedec(x, wavelet, mode="per")
    sigma = mad(coeff[-level])
    uthresh = sigma * np.sqrt(2 * np.log(len(x)))
    coeff[1:] = (pywt.threshold(i, value=uthresh, mode="soft") for i in coeff[1:])
    return pywt.waverec(coeff, wavelet, mode="per")

