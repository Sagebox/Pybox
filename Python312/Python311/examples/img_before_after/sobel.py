import scipy
import scipy.ndimage as ndimage
import numpy as np


def filter(img) :
    Kx = np.array([[-1, 0, 1], 
                 [-2, 0, 2], 
                 [-1, 0, 1]])

    Ky = np.array([[1, 2, 1], 
                   [0, 0, 0], 
                   [-1, -2, -1]])

    Ix = ndimage.convolve(img, Kx,output = float) # Get X plane
    Iy = ndimage.convolve(img, Ky,output = float) # Get Y Plane

    G = np.sqrt(np.square(Ix) + np.square(Iy))    # Get gradient

    G = G/(G.max()*.5)        # brighten it a little

    # The value below is multiplued by 255 to make standard RGB bitmap (floating-point)
    # with values from 0-255.
    #
    # Without this, the values would range from 0-1. 
    # This works with img_view() and img_before_after() when the 'normalize=True'
    # keyword is used (i.e. when the *255 is omitted).

    G = np.clip(G,0,1)*255        # clip is since values can go over 1.0

    return G  # return the new image (floating-point RGB image)


if __name__ == "__main__" :
    print("Error: This is a Sobel Filter module and is not meant to be run as a main program.")
    quit()

