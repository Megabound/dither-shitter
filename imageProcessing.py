# Dealing with manipulating images
import numpy as np
import masks # our own masks.py file
import cv2

# performs the current dither algo on a single image
def dither(mask, img, chunkSize):
    # create the output the same shape as the input, take note of the height and width
    output = np.zeros(img.shape) 
    height = len(output) 
    width = len(output[0])      
    # get our mask matrix and matix offset for applying the dither
    maskMatrix, xOffset = masks.makeMaskMatrix(mask, chunkSize) 
    maskHeight = len(maskMatrix)
    maskWidth = len(maskMatrix[0])
    # iterate through every X pixels in the image where X is the chunk size.
    for y in range(0, height, chunkSize): 
        for x in range(0, width, chunkSize):
            # calculate the image coordinates where the dither mask is to be applied, this is an N x N square where N is the chunk size                                    
            chunkXEnd = x + (chunkSize - 1)
            if chunkXEnd > width - 1:
                workingXSize = chunkXEnd = (width - 1)
            else:
                workingXSize = chunkSize
                        
            chunkYEnd = y + (chunkSize - 1)
            if chunkYEnd > height - 1:
                workingYSize = chunkYEnd - (height - 1)                 
            else:
                workingYSize = chunkSize

            # using the mask values above find out the current averaged pixel value in our moving N x N window
            currentValue = np.average(np.add(img[y : y + workingYSize, x : x + workingXSize],output[y : y + workingYSize, x : x + workingXSize]))
            # threshold the image, if it's under 127 make it black, over make it white
            newValue = 0 if currentValue < 127 else 255 
            output[y : y + workingYSize, x : x + workingXSize] = newValue 
            # calcualte the difference between the new value of the pixels and the old value
            error = currentValue if (newValue == 0) else currentValue - 255

            # get our error distribution mask by multiplying our error mask by the error calculated
            distributionMask = np.multiply(maskMatrix, error)

            # make sure our mask fits in the space we have and trim it down if we need to
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
            
            # apply the mask to the output
            output[y : y+rowCount, imgXStart : imgXStart+columnCount] += distributionMask[0 : rowCount, maskXStart : maskXStart+columnCount]
                            
    return output

# puts colour back into a dithered image
def colourise(img, dImg):           
    # create a mask where all black values are true and all white values are false. Convert this back to an integer, this way black will be represented by 1, and white by 0
    mask = dImg == 0
    mask = mask.astype('u8')
    output = img.copy()
    
    # for the red, green and blue layers in the colour image, mutliply it by the mask. This will copy the colour data into the black areas
    for x in range(len(img[0][0])):
        output[:,:,x] *= mask        

    # convert our inverted black areas back into white areas. The inversion happens when creating the truth mask
    height = len(output) 
    width = len(output[0])  
    for y in range(height):
        for x in range(width):
            if np.equal(output[y,x,:], [0, 0, 0]).all():
                output[y,x,:] = [255, 255, 255]

    return output  

# main processing pipeline
def pipeline(originalImage, doColourise, mask, chunkSize):    
    # convert the image to greyscale and create the dither mask
    imgGreyScale = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)    
    dithered = dither(mask, imgGreyScale, chunkSize)
    
    # return just the dither mask if we're not colourising
    if not doColourise:
        return dithered    
    
    # if we're here then we're meant to be colourising the output, do that
    colourised = colourise(originalImage, dithered)
    return colourised