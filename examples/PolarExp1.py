
# example
# Author: Ding, Liang
# Email: liangding86@gmail.com

from DRTRTMApps.DPolarScanner import DScanPolarity
import numpy as np

ampArr = np.random.random_sample([30, 3])
wndLens = 5
step = 3
VVArr = DScanPolarity(ampArr=ampArr, wndLens=wndLens, step=step)

import matplotlib.pyplot as plt
plt.figure(1)
plt.subplot(121)
plt.plot(VVArr[:, 0], 'r-', VVArr[:, 1], 'k^-', VVArr[:, 2], 'bD-.')
plt.title('Mean vector')

plt.subplot(122)
variance = np.sqrt(np.power(VVArr[:, 3], 2) + np.power(VVArr[:, 4], 2) + np.power(VVArr[:, 5], 2))
plt.plot(variance)
plt.title('Average deviation')

plt.show()

