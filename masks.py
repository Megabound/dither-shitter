import numpy as np

def makeMaskMatrix(mask):
    maskLength = len(mask)
    minX = int(np.min(mask[:,0]))
    maxX = int(np.max(mask[:,0]))
    minY = int(np.min(mask[:,1]))
    maxY = int(np.max(mask[:,1]))
    output = np.zeros(((maxY-minY)+1,(maxX-minX)+1))
    for i in range(maskLength):
        workingX = int(mask[i][0]) - minX
        workingY = int(mask[i][1])
        output[workingY][workingX] = mask[i][2]
    return output, minX