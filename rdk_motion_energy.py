from psychopy import core, data, event, visual, gui, monitors
import os
from pathlib import Path
from psychopy.hardware import keyboard
from psychopy.tools.monitorunittools import deg2pix
from scipy.ndimage import maximum_filter
import numpy as np
from numpy.fft import fftn, fftshift, fftfreq
from scipy.ndimage import rotate
import seaborn as sns
import matplotlib.pyplot as plt
import motionenergy as me
import stimulus as stim
from itertools import zip_longest
import numpy.ma as ma

## function to compute mean by frame
## input: xx = list
## output: list = mean of the ith elements of xx
def mean_iwise(xx):
    n_frame = [item.shape[0] for item in xx]
    mean = []
    for f in range(np.max(n_frame)):
        k = 0
        x = 0
        for i in range(len(xx)):
            if n_frame[i] > f:
                k += 1
                x += xx[i][f]
        mean.append(x/k)
    return(mean)

##  load data
expInfo={'participant':''}
expName="RDK"
dlg=gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
_thisDir =  os.path.abspath(os.getcwd())
data_dir = _thisDir + os.sep + 'data' + os.sep + expInfo['participant']  
data_array = np.load(data_dir + os.sep +  expInfo['participant'] + '.npy', allow_pickle=True,)


#  Determine the parameters of the display
mon1 = monitors.Monitor('testMonitor')
mon1.setDistance(50) #cm
mon1.setWidth(30) #cm
mon1.setSizePix([800, 600])
mon1.saveMon()

## compute ppd
ppd = int(deg2pix(1, mon1, correctFlat=False)) ## for monitor= mon1
framerate = 1 / 60  # display temporal resolution
number_of_dots =  data_array[0,7].shape[1]

## filters
filter_shape = 64, 64, 25 
filter_res = 1 / ppd, 1 / ppd, framerate
filters = me.motion_filters(filter_shape, filter_res, csigx=0.35, k=125) ## create filters
data_right = data_array[np.where(data_array[:,3] == 'a')]
data_left = data_array[np.where(data_array[:,3] == 'p')]
      
energy_right = []
for i in range(data_right.shape[0]): ##for each trial
      dots = data_array[i,7] ##dots frames for trial i
      dots_energy = me.apply_motion_energy_filters(dots, filters) ## apply filters on trial i
      energy = np.sum(dots_energy, axis=(0, 1)) ## motion energy on trial i
      energy = energy.astype(float)
      energy_right.append(energy)

right_mean = mean_iwise(energy_right)

energy_left = []
for i in range(data_left.shape[0]): ##for each trial
      dots = data_array[i,7] ##dots frames for trial i
      dots_energy = me.apply_motion_energy_filters(dots, filters) ## apply filters on trial i
      energy = np.sum(dots_energy, axis=(0, 1)) ## motion energy on trial i
      energy = energy.astype(float)
      energy_left.append(energy)

left_mean = mean_iwise(energy_left)

n = np.max([len(right_mean), len(left_mean)])
right_array = np.array(right_mean)[:n-1]
left_array = np.array(left_mean)[:n-1]
kernel = left_array - right_array
n = kernel.shape[0]


f, ax = plt.subplots()
x = np.linspace(1, n, n)
y = kernel
ax.plot(x, y)
ax.set(xlabel="time",
       ylabel="sensory weights (a.u.)")
plt.show()
plt.close('all')
