

import csv
import numpy as np


def DReadCSV(filePath):
     return np.genfromtxt(filePath, delimiter=',')



if __name__ == '__main__':
    filepath = '/home/dingl/database/RTRTM/Forward/Tst01_sta_XYZ.csv'
    dat = DReadCSV(filePath=filepath)

    print(dat[0])
