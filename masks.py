#dealing with manipulating masks
import numpy as np

# takes a dither mask input and inflates to to the chunk size being used
def makeMaskMatrix(mask, size):
    # take a note of how many operations the mask has (one operation is the distribution of error to a single pixel)
    maskLength = len(mask)
    # find the max and min x and y coordinates the mask contains
    minX = int(np.min(mask[:,0]))
    maxX = int(np.max(mask[:,0]))
    minY = int(np.min(mask[:,1]))
    maxY = int(np.max(mask[:,1]))
    # create an output mask scaled by the chunk size
    output = np.zeros((((maxY-minY)+1) * size,((maxX-minX)+1) * size))
    # fill in N x N sections of mask with the same distribution where N is chunk size
    for i in range(maskLength):
        workingX = int(mask[i][0]) - minX
        workingY = int(mask[i][1])
        startX = workingX * size
        startY = workingY * size
        output[startY : startY + size, startX : startX + size] = mask[i][2]
    return output, minX * size