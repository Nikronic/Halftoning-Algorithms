# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 21:46:18 2018

@author: HaMeD
"""

try:
    import Image, ImageDraw, ImageStat
except ImportError as e:
    try:
        import PIL.Image as Image
        import PIL.ImageDraw as ImageDraw
        import PIL.ImageStat as ImageStat
    except:
        raise
except:
    raise
import os


class Halftone(object):

    def __init__(self, path):
        self.path = path

    def make(self, sample=10, scale=1, percentage=0, filename_addition='_halftoned', angles=[0,15,30,45], style='color', antialias=False):
		
		
	def gcr(self, im, percentage):
        """
        Basic "Gray Component Replacement" function. Returns a CMYK image with
        percentage gray component removed from the CMY channels and put in the
        K channel, ie. for percentage=100, (41, 100, 255, 0) >> (0, 59, 214, 41)
        """
        cmyk_im = im.convert('CMYK')
        if not percentage:
            return cmyk_im
        cmyk_im = cmyk_im.split()
        cmyk = []
        for i in range(4):
            cmyk.append(cmyk_im[i].load())
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                gray = min(cmyk[0][x,y], cmyk[1][x,y], cmyk[2][x,y]) * percentage / 100
                for i in range(3):
                    cmyk[i][x,y] = cmyk[i][x,y] - gray
                cmyk[3][x,y] = gray
        return Image.merge('CMYK', cmyk_im)
		
	def halftone(self, im, cmyk, sample, scale, angles, antialias):
        
		
if __name__ == '__main__':
    
    import halftone
    
    h = Halftone('C:/Users/HaMeD/Desktop/lion_art_colorful_122044_3840x2160.jpg')
    h.make(angles=[25,32,0,12])