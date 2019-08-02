import PIL.Image as Image
import matplotlib.pyplot as plt
import numpy as np

def error_diffusion( pixel, size=(1,1) ):
    for y in range(0, size[1]-1):
        for x in range(1, size[0]-1):
            oldpixel = pixel[x, y]
            if oldpixel > 127:
                pixel[x, y] = 255
            else:
                pixel[x, y] = 0
                
            quant_error = oldpixel - pixel[x,y]
            pixel[x+1,y] = pixel[x+1,y] + (int)(7/16.0 * quant_error)
            pixel[x-1, y+1] = pixel[x-1,y+1] + (int)(3/16.0 * quant_error)
            pixel[x,y+1] = pixel[x,y+1] + (int)(5/16.0 * quant_error)
            pixel[x+1,y+1] = pixel[x+1,y+1] + (int)(1/16.0 * quant_error)
    print(np.asarray(pixel))
           
             
            
if __name__ == "__main__":
  img=Image.open('C:/Users/Hamed/Desktop/Halftoning/halftone algorithm/val_256/val_256/Places365_val_00004268.jpg')
  im=img.convert('CMYK')
  im = im.split()
  dots = []
  for chan in im:
      error_diffusion( chan.load(), chan.size )
  im = Image.merge("CMYK", im).convert("RGB")
  imgplot = plt.imshow(im)
  plt.show()
  im.save('my_image.png')
  