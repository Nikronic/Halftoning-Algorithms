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

    def make(self):
        f, e = os.path.splitext(self.path)

        outfile = "%s%s%s" % (f, '_halftoned', e)

        try:
            im = Image.open(self.path)
        except IOError:
            raise
            
        angles = [] 
        for j in range(4): 
            angles.append(random.randint(0, 90))
        
        sample = random.randint(5,15)
        
        cmyk = im.convert('CMYK')
        dots = self.halftone(im, cmyk, sample, angles, shape =random.getrandbits(1))
        new = Image.merge('CMYK', dots)

        new.save(outfile)

    def halftone(self, im, cmyk, sample, angles, shape):

        cmyk = cmyk.split()
        dots = []

        for channel, angle in zip(cmyk, angles):
            channel = channel.rotate(angle, expand=1)
            size = channel.size[0], channel.size[1]
            half_tone = Image.new('L', size)
            draw = ImageDraw.Draw(half_tone)

            # Cycle through one sample point at a time, drawing a circle for
            # each one:
            for x in range(0, channel.size[0], sample):
                for y in range(0, channel.size[1], sample):

                    # Area we sample to get the level:
                    box = channel.crop((x, y, x + sample, y + sample))

                    # The average level for that box (0-255):
                    mean = ImageStat.Stat(box).mean[0]

                    # The diameter of the circle to draw based on the mean (0-1):
                    diameter = (mean / 255) ** 0.5

                    # Size of the box we'll draw the circle in:

                    # Diameter of circle we'll draw:
                    # If sample=10 and scale=1 then this is (0-10)
                    draw_diameter = diameter * sample

                    # Position of top-left of box we'll draw the circle in:
                    # x_pos, y_pos = (x * scale), (y * scale)
                    box_x, box_y = x , y

                    # Positioned of top-left and bottom-right of circle:
                    # A maximum-sized circle will have its edges at the edges
                    # of the draw box.
                    x1 = box_x + ((sample - draw_diameter) / 2)
                    y1 = box_y + ((sample - draw_diameter) / 2)
                    x2 = x1 + draw_diameter
                    y2 = y1 + draw_diameter
                    
                    if shape is 1:
                        draw.ellipse([(x1, y1), (x2, y2)], fill=255)
                    else:
                        draw.rectangle([(x1, y1), (x2, y2)], fill=255)


            half_tone = half_tone.rotate(-angle, expand=1)
            width_half, height_half = half_tone.size

            # Top-left and bottom-right of the image to crop to:
            xx1 = (width_half - im.size[0]) / 2
            yy1 = (height_half - im.size[1]) / 2
            xx2 = xx1 + im.size[0]
            yy2 = yy1 + im.size[1]

            half_tone = half_tone.crop((xx1, yy1, xx2, yy2))

            dots.append(half_tone)
        return dots
    
if __name__ == '__main__':
    
    import random
    
    h = Halftone('F:/pictures/images/rsz_img_20160714_012739.jpg')
    h.make()
    