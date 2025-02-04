from PIL import Image
from PIL import ImageOps
import numpy as np
import binascii

with open('../uxn/test.icn', 'rb') as f:
    chunks = [chunk for chunk in iter(lambda: f.read(8), b'')]
    # for chunk in iter(lambda: f.read(8), b''):
        # b = binascii.hexlify(chunk)
    # Gotta figure something out here. How to collect these chunks into a convertable image?
    # can get this 8x8 by 8x8 and concatenate into rows, then concat the rows. 
    # How to know when a row ends though? Noodles have 48 8x8 images. Let's start with that.


# Mode is '1' for 1-bit
i = ImageOps.invert(Image.frombytes(mode='1', size=[8,8], data=chunk))
i.save('test.png')