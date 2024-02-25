#dealing with manipulating masks
import numpy as np

def makeMaskMatrix(mask, size):
    maskLength = len(mask)
    minX = int(np.min(mask[:,0]))
    maxX = int(np.max(mask[:,0]))
    minY = int(np.min(mask[:,1]))
    maxY = int(np.max(mask[:,1]))
    output = np.zeros((((maxY-minY)+1) * size,((maxX-minX)+1) * size))
    for i in range(maskLength):
        workingX = int(mask[i][0]) - minX
        workingY = int(mask[i][1])
        startX = workingX * size
        startY = workingY * size
        output[startY : startY + size, startX : startX + size] = mask[i][2]
    return output, minX * size