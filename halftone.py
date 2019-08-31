import PIL.Image as Image
import numpy.matlib
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

dithMat =[ 
    # 8x8 dispresed
    [[ 1, 30, 8, 28, 2, 29, 7, 27],
     [ 17, 9, 24, 16, 18, 10, 23, 15],
     [ 5, 25, 3, 32, 6, 26, 4, 31],
     [ 21, 13, 19, 11, 22, 14, 20, 12],
     [ 2, 29, 7, 27, 1, 30, 8, 28],
     [ 18, 10, 23, 15, 17, 9, 24, 16],
     [ 6, 26, 4, 31, 5, 25, 3, 32],
     [ 22, 14, 20, 12, 21, 13, 19, 11]],
    # 5x5 clockwise sprial
    [[3, 10, 16, 11, 4],
     [ 9, 20, 21, 17, 12],
     [ 15, 24, 25, 22, 13],
     [ 8, 19, 23, 18, 5],
     [ 2, 7, 14, 6, 1]],
    
    [[0, 8, 2, 10], 
     [12, 4, 14, 6],
     [3, 11, 1, 9],
     [15, 7, 13, 5]],
    
    [[0, 32, 8, 40, 2, 34, 10, 42],
     [48, 16, 56, 24, 50, 18, 58, 26],
     [3, 35, 11, 43, 1, 33, 9, 41],
     [51, 19, 59, 27, 49, 17, 57, 25]]
]

def gcr(im):
    cmyk_im = im.convert('CMYK')
    cmyk_im = cmyk_im.split()
    cmyk = []
    check_brightness = []
    for i in range(4):
        cmyk.append(np.asarray(cmyk_im[i]))
        check_brightness.append(np.mean(cmyk[i]) > 128)
    cmyk = np.asarray(cmyk)
    check_brightness = np.asarray(check_brightness)
    if np.mean(check_brightness) > 0.5:
        percentage = round(random.uniform(0.1,0.5),1)
    else:
        percentage = round(random.uniform(0.5,0.9),1)
        
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            gray = min(cmyk[0][x,y], cmyk[1][x,y], cmyk[2][x,y])* (100/100)
            for i in range(3):
                cmyk[i][x,y] = cmyk[i][x,y] - gray
            cmyk[3][x,y] = gray
    cmyk_final = []
    for i in range(4):
        cmyk_final.append(Image.fromarray(cmyk[i]).convert('L'))
    return Image.merge('CMYK', cmyk_final)

def get_resDmat(channel_size,dithMat):
    newSzY,newSzX = channel_size[1],channel_size[0]
    minDmat = min(min(dithMat))
    maxDmat = max(max(dithMat))
    nbOfIntervals = maxDmat-minDmat+2
    singleInterval = 255/nbOfIntervals
    scaledDithMat = np.multiply(np.subtract(dithMat , minDmat+1),singleInterval)
    scaledDithMat = scaledDithMat.astype(int)


    dmatSzY, dmatSzX = len(scaledDithMat),len(scaledDithMat[0])
    nX = math.ceil(newSzX / dmatSzX) 
    nY = math.ceil(newSzY / dmatSzY)
    resDmat = np.matlib.repmat(scaledDithMat.astype(int), nY, nX)[:newSzY,:newSzX]
    return resDmat

def generate_halftone(im,):
    cmyk_im = gcr(img)
    dithMat_sample = dithMat[random.randint(0,3)]
    cmyk = cmyk_im.split()
    angles = [[75,15,0,45],
              [45, 15, 0, 75],
              [75,45,0,15]]
    
    angles = angles[random.randint(0,2)]
    if cmyk[0] == cmyk[1] == cmyk[2] :
        angles = angles[:1]*4
    dots = []
    for x,i in enumerate(cmyk):
        channel_Rotation = i.rotate(angles[x], expand=1)
        #print(channel_Rotation.size)
        channel = np.asarray(channel_Rotation) > get_resDmat(channel_Rotation.size,dithMat_sample)
        channel = Image.fromarray(channel * 255).convert('L').rotate(-angles[x],expand=1)
        #channel = channel.rotate(-angles[x],expand=1)
        w,h = channel.size
        im_x,im_y = i.size
        x1 = (w-im_x)/2
        y1 = (h-im_y)/2
        channel = channel.crop((x1, y1, x1+im_x, y1+im_y))
        dots.append(channel)
    
    halftoned_im = Image.merge('CMYK',dots)
    
    return halftoned_im.convert('RGB')