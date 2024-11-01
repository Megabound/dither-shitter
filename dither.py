import os # file system stuff
import cv2 # image loading and manipulation
import numpy as np # quick matrix math
import tkinter as tk # for using a file dialog
from tkinter import filedialog # the file dialog part
import imageio as io # saving gifs
import pathlib # getting file extensions
import imageProcessing as ip # our imageProcessing.py file
import time # For accessing system time for timing

# Different masks that can be applied
ATKINSONMASK = np.array(([1,0,1/8],[2,0,1/8],[-1,1,1/8],[0,1,1/8],[1,1,1/8],[0,2,1/8]))
FLOYDMASK    = np.array(([1,0,7/16],[-1,1,3/16],[0,1,5/16],[1,1,1/16]))
CALEBMASK    = np.array(([1,0,2/8],[2,0,1/8],[-1,1,1/8],[0,1,2/8],[1,1,1/8],[0,2,1/8]))

# User options
MASK = ATKINSONMASK # which mask to use
COLOURISEVIDEO = False # should the output for video include colour?
COLOURISESTILL = True # should the output for stills include colour?
CHUNKSIZE = 2 # How chunky to make the output, 1 is no chunking. Positive numbers only, not 0
GIFFPS = 0 # What FPS should the gif play at? 0 is original FPS.
# ------------

# used for processing videos to gifs
def processVideo(fullPath):
    # use OpenCV to parse the video
    video = cv2.VideoCapture(fullpath)
    
    # if the user hasn't supplied an output framerate then use the videos own framerate
    if GIFFPS == 0:
        framesPerSecond = video.get(cv2.CAP_PROP_FPS)
    else:
        framesPerSecond = GIFFPS

    filename = os.path.basename(fullpath)
    directory = os.path.dirname(fullpath)

    # read individual frames and save them in the frames array
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

    # iterate through each frame in turn, converting it to a dithered output, when done put it in the output array
    for x in range(frameCount):
        print('Processing frame ', x)
        output[x] = ip.pipeline(frames[x], COLOURISEVIDEO, MASK, CHUNKSIZE)    
        if COLOURISEVIDEO:
            output[x] = cv2.cvtColor(output[x], cv2.COLOR_BGR2RGB) 

    # save the gif to file
    print("Saving GIF file")
    io.mimsave(os.path.join(directory, '_g' + str(CHUNKSIZE) + filename), output, loop=0, duration = 1000 * 1/framesPerSecond)

# used for processing single images
def processImage(fullPath):
    # use OpenCV to parse the image
    original = cv2.imread(fullpath)
    filename = os.path.basename(fullpath)
    directory = os.path.dirname(fullpath)
    # dither the image and save it to disk
    output = ip.pipeline(original, COLOURISESTILL, MASK, CHUNKSIZE)
    cv2.imwrite(os.path.join(directory, '_s' + str(CHUNKSIZE) + filename), output)    

#-------------------------Entry-------------------------------#

# Open a file picker, check to see if anything was chosen
root = tk.Tk()
root.withdraw()
fullpath = filedialog.askopenfilename()

if fullpath == '':
    quit()

filetype = pathlib.Path(fullpath).suffix

# Take note of the current time, for timekeeping
start_time = time.time()

# If it's a gif process as video, otherwise process as stills 
if filetype.lower() == '.gif':
    processVideo(fullpath)
else:
    processImage(fullpath)

# Check the time again and calculate elapsed time
print("--- %s seconds ---" % (time.time() - start_time))