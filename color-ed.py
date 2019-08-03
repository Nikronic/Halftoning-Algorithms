# %% libraries
import PIL.Image as Image
import numpy.matlib
import random


def error_diffusion(pixel, size=(1, 1)):
    for y in range(0, size[1] - 1):
        for x in range(1, size[0] - 1):
            oldpixel = pixel[x, y]
            if oldpixel > 127:
                pixel[x, y] = 255
            else:
                pixel[x, y] = 0

            quant_error = oldpixel - pixel[x, y]
            pixel[x + 1, y] = pixel[x + 1, y] + int(7 / 16.0 * quant_error)
            pixel[x - 1, y + 1] = pixel[x - 1, y + 1] + int(3 / 16.0 * quant_error)
            pixel[x, y + 1] = pixel[x, y + 1] + int(5 / 16.0 * quant_error)
            pixel[x + 1, y + 1] = pixel[x + 1, y + 1] + int(1 / 16.0 * quant_error)

def generate_halftone(img):
  img = img.convert('CMYK')
  img = img.split()
  angles = [[15, 45, 0, 75],
            [15,75,0,45],
            [75, 15, 0, 45]]

  angles = angles[random.randint(0, len(angles) - 1)]
  for x,chan in enumerate(img):
      chan.rotate(angles[x], expand=1)
      error_diffusion(chan.load(), chan.size)
      chan.rotate(-angles[x], expand=1)
  img = Image.merge("CMYK", img).convert("RGB")
  return img

