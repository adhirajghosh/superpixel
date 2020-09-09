import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from imageio import imsave

def crop(img):
    mask = img>0
    coords = np.argwhere(mask)
    c0 = coords.min(axis=0)
    c1 = coords.max(axis=0) + 1 
    cropped = img[c0[0] : c1[0], c0[1]:c1[1]]
    return cropped
    
path = <path to your images>
seg_path = <path where the superpixels are saved>
crop_path = <path where the cropped superpixels are saved>

for i in os.listdir(path):
    
    image = cv2.imread(os.path.join(path, i))
    segments = slic(img_as_float(image), n_segments = 10, sigma = 100)
    for (j, seg) in enumerate(np.unique(segments)):
        directory = seg_path+i[6:9]+'/'
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
        #print ("[x] inspecting segment ", j)
        mask = np.zeros(image.shape[:2], dtype = "uint8")
        mask[segments == seg] = 255

        separate = cv2.bitwise_and(image, image, mask = mask)
        name = directory+i[6:9]+"_"+str(j)
        imsave("%s.jpg" % name, separate, format="jpg")
        
        cropped = crop(separate)
        crop_dir = crop_path+i[6:9]+'/'
        try:
            os.makedirs(crop_dir, exist_ok=True)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
        name_c = crop_dir+ i[6:9]+"_"+str(j)
        imsave("%s.jpg" % name_c, cropped, format="jpg")
