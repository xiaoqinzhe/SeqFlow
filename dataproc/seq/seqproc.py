"""
sequence data processing
"""

import numpy as np
from sklearn.preprocessing import MinMaxScaler
import copy
from sklearn.preprocessing import MinMaxScaler, StandardScaler



class BaseNormalizer:
    def __init__(self):
        pass

    def fit(self, x, y=None):
        return

    def fit_transform(self, x, y=None):
        return x

    def transform(self, x, y=None):
        return x

    def inverse_transform(self, x, y=None):
        return x

class DifferenceNormalizer(BaseNormalizer):
    def __init__(self, k, count=1):
        self.k = k
        self.count=count
        self.kx = None

    def fit(self, x):
        self.kx = x[:len(x)-self.k]

    def fit_transform(self, x):
        self.fit(x)
        return self.transform(x)

    def transform(self, x):
        return x[self.k:] - self.kx

    def inverse_transform(self, x):
        return x

class WindowNormalizer(BaseNormalizer):
    def __init__(self):
        self.rx = None
        self.ry = None

    def fit(self, x, y, ybase=None):
        self.rx = x[:, 0, :]
        if ybase is not None: self.ry = x[:, 0, ybase]
        else: self.ry = None

    def fit_transform(self, x, y, ybase=None):
        self.fit(x, y, ybase)
        return self.transform(x, y)

    def transform(self, x, y):
        # print(self.rx.shape, self.ry.shape)
        # print(x.shape, y.shape)
        for i in range(len(x)):
            for j in range(len(x[i][0])):
                if self.rx[i][j]: x[i,:,j]= x[i,:,j]/self.rx[i][j] - 1
                else: x[i, :, j] = x[i, :, j] - self.rx[i][j]
            if self.ry is None: continue
            if len(y.shape) == 2:
                for j in range(len(y[i])):
                    if self.ry[i][j]:
                        y[i, j] = y[i, j] / self.ry[i][j] - 1
                    else:
                        y[i, j] = y[i, j] - self.ry[i][j]
            elif len(y.shape) == 3:
                for j in range(len(y[i][0])):
                    if self.ry[i][j]:
                        y[i, :, j] = y[i, :, j] / self.ry[i][j] - 1
                    else:
                        y[i, :, j] = y[i, :, j] - self.ry[i][j]


        return x, y

    def inverse_transform(self, y, start=0, end=None):
        # if end is None: end = len()
        if self.ry is None: return y
        for i in range(len(y)):
            if y.ndim == 2:
                for j in range(len(y[i])):
                    if self.ry[start+i][j]:
                        y[i, j] = (y[i, j]+1) * self.ry[start+i][j]
                    else:
                        y[i, j] = y[i, j] + self.ry[start+i][j]
            elif y.ndim==3:
                for j in range(len(y[i][0])):
                    if self.ry[start + i][j]:
                        y[i, :, j] = (y[i, :, j] + 1) * self.ry[start + i][j]
                    else:
                        y[i, :, j] = y[i, :, j] + self.ry[start + i][j]
        return y

class SeqDP:
    def __init__(self, ):
        pass

    # differencing sequence
    def differencing(x, diff_count, period):
        tempx = copy.copy(x)
        for i in range(diff_count):
            tempx[period:] = tempx[period:] - tempx[0:len(tempx) - period]
            tempx = tempx[period:]
        return tempx

    def redifferencing(x, dx, diff_count):
        tempx = copy.copy(x)
        for i in range(diff_count):
            tempx[:] = tempx[:] + dx[:len(tempx)]
        return tempx

    # sliding window x, y
    def windowing_xy(self, x, y, n_xseq, dis, n_yseq=1):
        ns = len(y) - dis - n_xseq - n_yseq + 1 + 1
        dx, dy = [], []
        for i in range(ns):
            if n_xseq == 1: dx.append(x[i])
            else: dx.append(x[i: i + n_xseq])
            if n_yseq == 1: dy.append(y[i + n_xseq + dis - 1])
            else: dy.append(y[i + n_xseq + dis - 1: i + n_xseq + dis - 1 + n_yseq])
        return np.array(dx), np.array(dy)

    # sliding window for series x
    def windowing_x(self, x, n_seq):
        ns = (len(x) + 1 - n_seq)
        dx = []
        for i in range(ns):
            if n_seq == 1: dx.append(x[i])
            else: dx.append(x[i:i + n_seq])
        return np.array(dx)

    #  normalize window according first element
    def normalize_window_afe(x):
        for i in range(len(x)):
            x0 = x[i][0]
            if x0:
                x[i][:] = (x[i][:] - x0) / x0
            else:
                x[i][:] = x[i][:] - x0
        return x

    def smoothSeq(x, sm):
        a = np.zeros(len(x) - sm + 1, dtype=np.float32)
        for i in range(len(a)):
            a[i] = np.mean(x[i:i + sm])
        return a

    @classmethod
    def get_minmax_normalizer(cls, range=(0,1)):
        return MinMaxScaler(feature_range=range)

    @classmethod
    def get_standard_normalizer(cls):
        return StandardScaler()

    @classmethod
    def get_difference_normalizer(cls, k):
        return DifferenceNormalizer(k)

    @classmethod
    def get_win_normalizer(cls):
        return WindowNormalizer()

    # def renormalize(self, data, origin):
    # 	r=[]
    # 	for i in range(len(data)):
    # 		r.append([origin[i][0][0]*(data[i][0]+1)])
    # 		#print(origin[i][0][0], data[i][0][0])
    # 		#exit()
    # 	if isdifferencing: r=redifferencing(r, TimeSeriesDP.dy[TimeSeriesDP.bound-period:])
    # 	return r
    #
    # def renormalize2(self, data, origin):
    # 	data=TimeSeriesDP.yscaler.inverse_transform(data)
    # 	if isdifferencing: data = redifferencing(data, TimeSeriesDP.dy[TimeSeriesDP.bound-period:])
    # 	return data