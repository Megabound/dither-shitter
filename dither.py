import os
import cv2
import numpy as np
import tkinter as tk
import imageio as io
import pathlib
import imageProcessing as ip
from tkinter import filedialog
import time

ATKINSONMASK = np.array(([1,0,1/8],[2,0,1/8],[-1,1,1/8],[0,1,1/8],[1,1,1/8],[0,2,1/8]))
FLOYDMASK    = np.array(([1,0,7/16],[-1,1,3/16],[0,1,5/16],[1,1,1/16]))
CALEBMASK    = np.array(([1,0,2/8],[2,0,1/8],[-1,1,1/8],[0,1,2/8],[1,1,1/8],[0,2,1/8]))

# User options
MASK = ATKINSONMASK
COLOURISEVIDEO = False
COLOURISESTILL = False
# ------------

def pipeline(originalImage, doColourise):    
    imgGreyScale = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    dithered = ip.dither(MASK, imgGreyScale)
    
    if not doColourise:
        return dithered    
    
    colourised = colourise(originalImage, dithered)
    return colourised

def processVideo(fullPath):
    video = cv2.VideoCapture(fullpath)
    filename = os.path.basename(fullpath)
    directory = os.path.dirname(fullpath)
    frames = []
    ret, frame = video.read()  # ret=True if it finds a frame else False.
    while ret:
        # read next frame
        ret, frame = video.read()
        if not ret:
            break            
        frames.append(frame)

    frameCount = len(frames)
    output = frames.copy()

    for x in range(frameCount):
        print('Processing frame ', x)
        output[x] = pipeline(frames[x], COLOURISEVIDEO)

    print("Saving GIF file")
    io.mimsave(os.path.join(directory, '_g' + filename), output, loop=0, duration = 0.3)

def processImage(fullPath):
    original = cv2.imread(fullpath)
    filename = os.path.basename(fullpath)
    directory = os.path.dirname(fullpath)
    output = pipeline(original, COLOURISESTILL)
    cv2.imwrite(os.path.join(directory, '_s' + filename), output)    

## Entry ##

root = tk.Tk()
root.withdraw()
fullpath = filedialog.askopenfilename()

if fullpath == '':
    quit()

filetype = pathlib.Path(fullpath).suffix

start_time = time.time()

if filetype.lower() == '.gif':
    processVideo(fullpath)
else:
    processImage(fullpath)

print("--- %s seconds ---" % (time.time() - start_time))