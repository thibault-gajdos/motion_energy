import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq
import motionenergy as me
from numpy.fft import fftn, ifftn, fftshift

# set size and shape of the filternx,
nx, nt = 41, 41
dx, dt = 1/23, 1/60
size = nx, 1, nt #ny = 1, so only in the (x,t) dimensions
res = dx, dx, dt

k_range = np.arange(70, 150, 1)
s_range = np.arange(.2, .4, .01)
space = np.empty((k_range.shape[0],s_range.shape[0]))
time = np.empty((k_range.shape[0],s_range.shape[0]))

for i, k in enumerate(k_range):
    for j, s in enumerate(s_range):
        filters = me.motion_filters(size, res, k=k, csigx=s) #Create filters
        filt = filters[0] #select right/even
        filt_fft = np.abs(fftshift(fftn(filt)).squeeze()) #fourier transform of the filter
        fxs = fftshift(fftfreq(nx, dx)) #spatial spectral mesh
        fts = fftshift(fftfreq(nt * 2 - 1, dt)) #temporal sepctral mesh
        m = np.unravel_index(np.argmax(filt_fft), filt_fft.shape) # prefered frequencies
        space[i,j] = fxs[m[0]] #spatial freq in cyc/deg
        time[i,j] = fts[m[1]] ## temporal freq in cyc/s

speed = time/space
target_speed = 9
tol_speed = .3
speed_min = target_speed - tol_speed
speed_max = target_speed + tol_speed
coord = np.where((abs(speed) >speed_min) & (abs(speed)<speed_max))


# The filter is causal in time, so crop off the first half
# filt = filt.squeeze()[:, nt:]
# Plot the spectral representations of the filter
# f, ax2 = plt.subplots()
# ax2.pcolormesh(fxx, ftt, filt_fft)
# plt.show()
