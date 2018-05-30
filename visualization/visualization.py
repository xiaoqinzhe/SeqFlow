import matplotlib.pyplot as plt

def plotSerieses(x, w, h, name = None):
    fig = plt.figure(name)
    axes = fig.subplots(w, h)
    for i in range(w):
        for j in range(h):
            if i*w+j >= len(x): return
            axes[i][j].plot(x[i*w+j])

def scatterSeries(x, y, z=None, dim = 2, color = None, name = None):
    fig = plt.figure(name)
    if dim == 2: plt.scatter(x, y, c=color)
    elif dim == 3:
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(x, y, z, c=color)

