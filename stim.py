# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 12:01:59 2020

@author: mservant
"""

from psychopy import core, data, event, visual, gui
import numpy as np
import os
from pathlib import Path
from psychopy.hardware import keyboard
from psychopy.preferences import prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound
import serial
import time 


port_usb_serie = serial.Serial(port ="COM3",baudrate =115200)

def read_port():
    port_usb_serie.write(b'i')
    port_usb_serie.flush()
    time.sleep(.05) 
    didier = port_usb_serie.in_waiting#Return the number of bytes currently in the input buffer
    # port_usb_serie.flush()
    mat = port_usb_serie.read(didier)
    mat = mat.decode()
    mat = mat.split('\r\n')
    return mat


# for i in range (20):
#     print ("")
#     print (i)
#     print (read_port())

def get_baseline():
    base = read_port()
    base_left = float(base[2][33:])
    base_right = float(base[3][32:])
    return base_left, base_right

def change_grams_relative(value_left, value_right):
    value_left = int(np.round(value_left))
    value_right = int(np.round(value_right))
    base_left, base_right = get_baseline()
    base_left = int(np.round(base_left))
    base_right = int(np.round(base_right))
    adjusted_value_left = base_left+value_left
    adjusted_value_right = base_right+value_right
    output_left = str(adjusted_value_left) + 'd'
    output_left = output_left.encode()
    output_right = str(adjusted_value_right) + 'g'
    output_right = output_right.encode()    
    port_usb_serie.write(output_left)
    port_usb_serie.write(output_right)
    time.sleep(.05) 
    print (base_left, base_right)
#    print(adjusted_value_left,adjusted_value_right)
    
    

expName="RDK_force"
expInfo={'participant':''}
date_exp = data.getDateStr() 
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName, order=['participant'])
if dlg.OK==False: core.quit() #user pressed cancel



win = visual.Window(fullscr=True, monitor='mathieu',size=(1920, 1080), color=[0,0,0], colorSpace='rgb255', units='deg')
police = 'Consolas' #monospaced font
win.setMouseVisible(False) #hide the mouse cursor!!!




# initialize keyboards
resp = keyboard.Keyboard()
defaultKeyboard = keyboard.Keyboard()#for escaping only



#######################Parameters for RDK stimuli
framerate = 60.0
speed_deg_sec =8.#8.0 #in degrees/s 12 in Pilly in Seitz
dot_density = 16.7#in deg-2 s-1
rayon_cercle = 9.0#in deg
number_of_dots = int(np.round(dot_density * np.pi * np.square(rayon_cercle) * (1/framerate)))
#######################

dots=visual.DotStim(win=win, name='random_dots',
    nDots= number_of_dots, 
    dotSize=4,#in pixels
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


coherence_trial = .4
current_direction = 0

dots.setFieldCoherence(coherence_trial)
dots.setDir(current_direction)     

mySound = sound.Sound('A', secs = 0.08)

change_grams_relative(3100,3100)

while True: 
    theseKeys = resp.getKeys(keyList=['g','d'], waitRelease=False)
    if defaultKeyboard.getKeys(keyList=["escape"], waitRelease=False):
        core.quit()
    if len(theseKeys):
        mySound.play()
        win.flip()
        core.wait(1.)
        resp.clearEvents(eventType='keyboard')
        change_grams_relative(3100,3100)
    dots.draw()
    win.flip()      

#100
#600
#1200
#1800
#2600

#100
#700
#1300
#1900
#2500
#3100

