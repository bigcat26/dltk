"""
Image preprocess tools
"""

import cv2
import numpy as np
from PIL import Image

def resize_image_ndarray(image: np.ndarray, size, letterbox: bool):
    """
    apply resize & letterbox to input numpy image
    """
    ih, iw, _   = np.shape(image)
    w, h        = size
    if letterbox:
        scale   = min(w/iw, h/ih)
        nw      = int(iw*scale)
        nh      = int(ih*scale)

        image   = cv2.resize(image, (nw, nh))
        new_image   = np.ones([size[1], size[0], 3]) * 128
        new_image[(h-nh)//2:nh+(h-nh)//2, (w-nw)//2:nw+(w-nw)//2] = image
    else:
        new_image = cv2.resize(image, (w, h))
    return new_image

def resize_image_pil(image: Image.Image, size, letterbox: bool):
    """
    apply resize & letterbox to input PIL image
    """
    iw, ih  = image.size
    w, h    = size
    if letterbox:
        scale   = min(w/iw, h/ih)
        nw      = int(iw*scale)
        nh      = int(ih*scale)

        image   = image.resize((nw,nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128,128,128))
        new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    else:
        new_image = image.resize((w, h), Image.BICUBIC)
    return new_image

def resize_image(image, size, letterbox: bool):
    """
    apply resize & letterbox to input image (auto adapt cv2, PIL and numpy image)
    """
    if isinstance(image, np.ndarray):
        return resize_image_ndarray(image, size, letterbox)
    elif isinstance(image, Image.Image):
        return resize_image_pil(image, size, letterbox)
    elif isinstance(image, cv2.Mat):
        raise RuntimeError('resizing cv2 image')
    else:
        raise RuntimeError('unknown image type')

def to_rgb_image(image):
    """
    convert grayscale image or image with alpha channel to RGB image
    """
    if len(np.shape(image)) == 3 and np.shape(image)[2] == 3:
        return image

    image = image.convert('RGB')
    return image
