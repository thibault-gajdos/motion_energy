Python 3.8.5 (default, Sep  4 2020, 02:22:02) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.19.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import numpy as np

In [3]: from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq

In [4]: 
In [5]: import motionenergy as me

In [6]: from numpy.fft import fftn, ifftn, fftshift

In [7]: from scipy import optimize

In [8]: from __future__ import division
    ... from collections import namedtuple
    ... from math import factorial
    ... import numpy as np
    ... from scipy.ndimage import rotate
    ... 
    ... 
    ... FilterSet = namedtuple("FilterSet", ["p1", "p2", "n1", "n2"])
    ... 
    ... 
    ... ...
    ... 
    ...     return energy_array
    ... 
    ... 
    ... def crop_convolved(a, shape):
    ...     """Crop an array to shape after circular convolution."""
    ...     start = np.subtract(a.shape, shape) // 2
    ...     end = np.add(start, shape)
    ...     indices = tuple(slice(s, e) for s, e in zip(start, end))
    ...     return a[indices]

In [9]: nx, nt = 41, 41

In [10]: dx, dt = .0436, .0133

In [11]: size = nx, 1, nt #ny = 1, so only in the (x,t) dimensions

In [12]: res = dx, .01, dt

In [13]: k = 130

In [14]: s = .45

In [15]: filters = me.motion_filters(size, res, k=k, csigx=s)

In [16]: filt = filters[2]

In [17]: filt_fft = np.abs(fftshift(fftn(filt)).squeeze())

In [18]: fxs = fftshift(fftfreq(nx, dx))

In [19]: fts = fftshift(fftfreq(nt * 2 - 1, dt))

In [20]: m = np.unravel_index(np.argmax(filt_fft), filt_fft.shape)

In [21]: xmax = fxs[m[0]]

In [22]: tmax = fts[m[1]]

In [23]: speed = tmax/xmax

In [24]: print(speed)
8.296667594913211

In [25]: k = 135

In [26]: s = .35

In [27]: filters = me.motion_filters(size, res, k=k, csigx=s)

In [28]: filt = filters[2]

In [29]: filt_fft = np.abs(fftshift(fftn(filt)).squeeze())

In [30]: fxs = fftshift(fftfreq(nx, dx))

In [31]: fts = fftshift(fftfreq(nt * 2 - 1, dt))

In [32]: m = np.unravel_index(np.argmax(filt_fft), filt_fft.shape)

In [33]: xmax = fxs[m[0]]

In [34]: tmax = fts[m[1]]

In [35]: speed = tmax/xmax

In [36]: print(speed)
9.12633435440453

In [37]: print(xmax) ##cyc/deg
-1.1188185276348175

In [38]: print(tmax) #cyc/s

In [39]: range(50,150)
Out[39]: range(50, 150)

In [40]: range(50:150)
  File "<ipython-input-40-7439e1d8bffb>", line 1
    range(50:150)
            ^
SyntaxError: invalid syntax


In [41]: 