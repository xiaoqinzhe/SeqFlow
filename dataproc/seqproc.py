"""
sequence data processing
"""

import numpy as np
from sklearn.preprocessing import MinMaxScaler
import copy
from sklearn.preprocessing import MinMaxScaler, StandardScaler

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
def windowing_xy(x, y, n_xseq, dis, n_yseq = 1):
    ns = len(y) - dis - n_xseq - n_yseq + 1
    dx, dy = [], []
    for i in range(ns):
        dx.append(x[i : i+n_xseq])
        if n_yseq == 1: dy.append(y[i+n_xseq+dis-1])
        else: dy.append(y[i+n_xseq+dis-1 : i+n_xseq+dis-1+n_yseq])
    return np.array(dx), np.array(dy)

# sliding window for series x
def windowing_x(x, n_seq):
    ns = (len(x)  + 1 - n_seq)
    dx = []
    for i in range(ns):
        dx.append(x[i:i + n_seq])
    return np.array(dx)

#  normalize window according first element
def normalize_window_afe(x):
    for i in range(len(x)):
        x0=x[i][0]
        if x0: x[i][:] = (x[i][:]-x0)/x0
        else: x[i][:] = x[i][:]-x0
    return x

def smoothSeq(x, sm):
    a = np.zeros(len(x) - sm + 1, dtype=np.float32)
    for i in range(len(a)):
        a[i] = np.mean(x[i:i + sm])
    return a

class BaseNormalizer:
    def __init__(self):
        pass

    def fit(self, x):
        return

    def fit_transform(self, x):
        return x

    def transform(self, x):
        return x

    def inverse_transform(self, x):
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

class SeqDP:
    def __init__(self, ):
        pass

    @classmethod
    def get_minmax_normalizer(cls, range=(0,1)):
        return MinMaxScaler(feature_range=range)

    @classmethod
    def get_standard_normalizer(cls):
        return StandardScaler()

    @classmethod
    def get_difference_normalizer(cls, k):
        return DifferenceNormalizer(k)


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