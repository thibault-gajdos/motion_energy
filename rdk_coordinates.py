# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 12:01:59 2020

@author: mservant
"""

from psychopy import core, data, event, visual, gui, monitors
import numpy as np
import pandas as pd
import os
from pathlib import Path
from psychopy.hardware import keyboard
from psychopy.tools.monitorunittools import deg2pix
from scipy.ndimage import maximum_filter

## * informations & files

## participant and expe info infos

expInfo={'participant':''}
expName="RDK"
expInfo['date'] = data.getDateStr()
dlg=gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK==False: core.quit() #user pressed cancel

_thisDir =  os.path.abspath(os.getcwd())
data_dir = _thisDir + os.sep + 'data' + os.sep + expInfo['participant']  
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
subject_id = expInfo['participant']

## create files
filename = data_dir + os.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
filename_short =  data_dir + os.sep + expInfo['participant']
output = "subject_id,trial,coherence_trial,pressed_rdk,expected_rdk,rt_rdk, accuracy_rdk, dots_coord\n"
running_filename = filename_short + '_TEMP.txt'

## * Hardware
##def monitor
mon1 = monitors.Monitor('testMonitor')
mon1.setDistance(50) #cm
mon1.setWidth(30) #cm
mon1.setSizePix([800, 600])
mon1.saveMon()
ppd = int(deg2pix(1, mon1, correctFlat=False)) ## ppd for monitor= mon1

## keyboard
kb = keyboard.Keyboard() # initialize keyboards

## * Stimuli
#create a window to draw in
win = visual.Window(fullscr=False, size=(800, 600), monitor = mon1, color=[0,0,0], colorSpace='rgb255', units='deg')
win.setMouseVisible(False) #hide the mouse cursor!!!

## Instructions
police = 'Consolas' #monospaced font
size_instruc = 1
instr_time = 0.1
too_late = visual.TextStim(win, ori=0,
                           height = size_instruc,
                           font = police,
                           color = 'red',
                           text = "Trop lent!")

## stimuli

fixation = visual.GratingStim(win=win, 
                              mask='cross', size=0.8, 
                              pos=[0,0], sf=0)

#######################Parameters for RDK stimuli
framerate = 60.0
speed_deg_sec =8 #9.0 #in degrees/s 12 in Pilly in Seitz; corresponds to the filters
dot_density = 16.7#in deg-2 s-1
rayon_cercle = 9.0#in deg
number_of_dots = int(np.round(dot_density * np.pi * np.square(rayon_cercle) * (1/framerate)))

dotsize = 4 ## because dots.dotSize = 2*dotsize
dots=visual.DotStim(win=win, name='random_dots',
    nDots= number_of_dots, 
    dotSize=dotsize,#in pixels
    units = 'deg',
    speed= speed_deg_sec/framerate,#in degrees per frame
    dir= 0, #in degrees  --> manipulated
    coherence= 0.0,#--> manipulated
    fieldPos=[0.0, 0.0],
    fieldSize=rayon_cercle*2,
    fieldShape='circle',
    signalDots='different', # on each frame the dots constituting the signal could be the same as on the previous frame or different. If 'same', participants may determine the direction of dots based on a single dot.
    noiseDots='position', #can be set to 'direction' or 'location'. 'location' has the disadvantage that the noise dots not only have a random direction but alos a random speed (whereas signal dots have a constant speed and constant direction)
    dotLife= -1,#number of frames each dot lives. 
    color=[255,255,255], colorSpace='rgb255')#color of the dots

## * trials handler
## possible_stim
direction_array = np.array([0, 180]) #direction: 0=right, 180=left
possible_stim = [[direction] for direction in direction_array]
n_trial = 100 ## number of trials 

##  sequence
seq = np.empty((0,2))
block = np.tile(possible_stim, n_trial).reshape(-1,2)
np.random.shuffle (block)
seq = np.append(block, seq).reshape(-1,2)

## *  Trials
## parameters
deadline = 3
ITI = 1
SOA = .2
cue_time = .3
coherence_trial = 0

## ** Main loop

## Initialisation
trial = 0
data_container = []
n_pix = int(2 * rayon_cercle * ppd) ##image size in pixels
grid = np.linspace(-rayon_cercle, rayon_cercle, n_pix) ##grid for mesh
xx, yy = np.meshgrid(grid, grid) ##mesh frame

for i in range(len(seq)):
    ## initialize
    pressed_rdk = -1
    expected_rdk = -1
    rt_rdk = -1
    accuracy_rdk = -1
    dots_coord = []

    dots.setFieldCoherence(coherence_trial)

    ## update trial and block number
    trial += 1
    ## define direction
    d_i = seq[i][0]
    ## draw cue
    fixation.draw()
    win.flip()
    core.wait(cue_time)
    win.flip()
    core.wait(SOA)

    dots.setDir(d_i)   ## set current direction
    ## expected responses
    if d_i == 0:
        expected_rdk = 'p'
    elif d_i == 180:
        expected_rdk = 'a'
    ## clear kb  buffer
    kb_delay = 0
    win.callOnFlip(kb.clock.reset)
    win.callOnFlip(kb.clearEvents, eventType='keyboard')    
    while True:
        if kb_delay==1:#check keyboard buffer AFTER first draw of stimulus and clock reset 
            t = kb.clock.getTime()
            if t > deadline:
                too_late.draw()
                win.flip()
                core.wait(1)
                break
            theseKeys = kb.getKeys(keyList=['a', 'p'], waitRelease=False)
            if len(theseKeys):
                theseKeys_rdk = theseKeys[0] 
                pressed_rdk = theseKeys_rdk.name
                rt_rdk = theseKeys_rdk.rt
                if expected_rdk == pressed_rdk:
                    accuracy_rdk = 1
                    break
                else:
                    accuracy_rdk = 0
                break
            if kb.getKeys(keyList=["escape"], waitRelease=False):
                core.quit()
        dots.draw()
        ## recover dots coordinate and translate them on a mesh
        current_frame =  np.zeros_like(xx) ##empty frame
        y = dots._verticesBase.transpose()
        i, j = np.round(y * ppd + rayon_cercle * ppd -  dotsize / 2).astype(np.int)
        current_frame[i, j] = 1 ##fill the mesh
        current_frame = maximum_filter(current_frame,  dotsize) ##build dots of size=dotsize        
        dots_coord.append(current_frame)
        win.flip()  
        if kb_delay == 0:
            kb.clearEvents(eventType='keyboard')
            kb_delay = 1    
    win.flip()
    dots_coord = np.stack(dots_coord,axis = -1)
    data_array = [subject_id,
                  trial,
                  coherence_trial,
                  pressed_rdk,
                  expected_rdk,
                  rt_rdk,
                  accuracy_rdk,
                  dots_coord
                  ]
            
    data_container.append(data_array)
 



    win.flip() # clean screen
    core.wait(ITI)

## ** compute thresh, save & cleanup
data_container = np.array(data_container, dtype=object)
np.save(filename, data_container)
np.save(filename_short, data_container)

win.close()
core.quit()




    
