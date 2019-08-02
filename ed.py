import PIL.Image as Image
import matplotlib.pyplot as plt


def gen_matrix(e):
    """ Generating new matrix.
    @param e The width and height of the matrix is 2^e.
    @return New 2x2 to 2^e x 2^e matrix list.
    """
    if e < 1:
      return None
    m_list = [[[1, 2], [3, 0]]]
    _b = m_list[0]
    for n in range(1, e):
        m = m_list[n - 1]
        m_list.append([
            [4 * i + _b[0][0] for i in m[0]] + [4 * i + _b[0][1] for i in m[0]],
            [4 * i + _b[0][0] for i in m[1]] + [4 * i + _b[0][1] for i in m[1]],
            [4 * i + _b[1][0] for i in m[0]] + [4 * i + _b[1][1] for i in m[0]],
            [4 * i + _b[1][0] for i in m[1]] + [4 * i + _b[1][1] for i in m[1]],
        ])
    return m_list


def ordered_dithering(pixel, size, matrix):
    """ Dithering on a single channel.
      @param pixel PIL PixelAccess object.
      @param size A tuple to represent the size of pixel.
      @param matrix Must be NxN, and N == 2^e where e>=1
    """
    X, Y = size
    N = len(matrix)

    T = [[255 * (matrix[x][y] + 0.5) / N / N for x in range(N)] for y in range(N)]
    for y in range(0, Y):
        for x in range(0, X):
            pixel[x, y] = 255 if pixel[x, y] > T[x % N][y % N] else 0


if __name__ == "__main__":
    img = Image.open('C:/Users/Hamed/Desktop/Halftoning/halftone algorithm/val_256/val_256/Places365_val_00004289.jpg')
    im = img.convert('CMYK')
    im = im.split()
    dots = []
    # for chan in im:
    # ordered_dithering( chan.load(), chan.size , gen_matrix(3)[3-1])
    im = Image.merge("CMYK", im).convert("RGB")
    imgplot = plt.imshow(im)
    plt.show()
    # im.save('my_image.png')
