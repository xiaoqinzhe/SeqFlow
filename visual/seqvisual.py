# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np

def plot_series(x, label=None, color=None, name=None):
    s = np.shape(x)
    print(s)
    if len(s)==1:
        fig = plt.figure(name)
        plt.plot(x, label=label, color=color)
        return
    if len(s)==2:
        x = [x]
    s=np.shape(x)
    if name is None: name = ""
    for dim in range(s[2]):
        name1 = name + "--dim: " + str(dim)
        fig = plt.figure(name1)
        for i, e in enumerate(x):
            if label is None: plt.plot(e[:, dim], color=color)
            else: plt.plot(e[:, dim], label=label[i], color=color)
        plt.legend(loc=0)

def subplot_series(x, w, h, name = None):
    fig = plt.figure(name)
    axes = fig.subplots(w, h)
    for i in range(w):
        for j in range(h):
            if i*w+j >= len(x): return
            axes[i][j].plot(x[i*w+j])

def scatter_series(x, y, z=None, color = None, name = None):
    fig = plt.figure(name)
    if z is None: plt.scatter(x, y, c=color)
    else:
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(x, y, z, c=color)


class SeqPredDataVisual:

    @classmethod
    def plot_series(cls, y, pred_y, showed=True):
        plot_series([y, pred_y], label=["goal", "predict"], name="Time Series Prediction")
        if showed: plt.show()

