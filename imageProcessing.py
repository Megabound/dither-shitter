##Dealing with manipulating images
import numpy as np
import masks
import cv2

def dither(mask, img):
    output = np.zeros(img.shape) 
    height = len(output) 
    width = len(output[0])      
    maskMatrix, xOffset = masks.makeMaskMatrix(mask) 
    maskHeight = len(maskMatrix)
    maskWidth = len(maskMatrix[0])
    for y in range(height): 
        for x in range(width):
            currentValue = img[y][x] + output[y][x] 
            newValue = 0 if currentValue < 127 else 255 
            output[y][x] = newValue 
            error = currentValue if (newValue == 0) else currentValue - 255
            
            distributionMask = np.multiply(maskMatrix, error)
            imgXStart = x + xOffset
            maskXStart = 0
            if imgXStart < 0:
                imgXStart = 0
                maskXStart = imgXStart - xOffset
            
            maskXEnd = x + maskWidth + xOffset
            if maskXEnd > (width - 1):
                columnCount = maskWidth - (maskXEnd - (width - 1)) - maskXStart
            else:
                columnCount = maskWidth - maskXStart

            maskYEnd = y + maskHeight
            if maskYEnd > (height - 1):
                rowCount = maskHeight - (maskYEnd - (height - 1))
            else:
                rowCount = maskHeight
            
            output[y : y+rowCount, imgXStart : imgXStart+columnCount] += distributionMask[0 : rowCount, maskXStart : maskXStart+columnCount]
                            
    return output

def colourise(img, dImg):    
    mask = dImg == 0
    mask = mask.astype('u8')
    output = img.copy()
    
    for x in range(len(img[0][0])):
        output[:,:,x] *= mask        

    height = len(output) 
    width = len(output[0])  
    for y in range(height):
        for x in range(width):
            if np.equal(output[y,x,:], [0, 0, 0]).all():
                output[y,x,:] = [255, 255, 255]

    return output  

def pipeline(originalImage, doColourise, mask):    
    imgGreyScale = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    dithered = dither(mask, imgGreyScale)
    
    if not doColourise:
        return dithered    
    
    colourised = colourise(originalImage, dithered)
    return colourised