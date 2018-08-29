# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Common used functions or class in data precessing procedure
"""


def time_filter(x,  start_time, end_time = None, time_index = 0):
    """ A time filter for selecting data from x starting from start_time to end_time

    Parameters
    ----------
    x : array-like, shape = [n_samples, n_features]
        filter data.

    start_time : datetime
        start time of x.
    
    end_time : datetime, optional, default None
        the end time of x.
        if None, it would be the largest time in x

    time_index : int, optional, default 0
        the time index of x.

    Returns
    -------
    x : array-like
        satisfied data x
    """

    if start_time is None: return x
    if start_time > end_time: raise AttributeError("start_time must be smaller than end_time")
    start_index, end_index = -1, -1
    for i in range(len(x)):
        # print(type(x[i][time_index]))
        # print(start_time)
        # exit()
        if x[i][time_index] == start_time:
            start_index = i
            break
    if start_index < 0:
        raise AttributeError("start_time is not in the x scope")
    if end_time is None:
        end_index = len(x) - 1
    else:
        for i in range(len(x)):
            if x[i][time_index] == end_time:
                end_index = i
                break
        if end_index < 0:
            end_index = len(x) - 1
            raise RuntimeWarning("end_time is not in the x scope")
    return x[start_index:end_index]
