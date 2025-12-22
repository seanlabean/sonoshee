from PIL import Image
from PIL import ImageOps
import argparse
import binascii
import numpy as np

def iterate_8x8_blocks(pixels_1d, height, width):
    """
    Args:
        pixels_1d (list or np.ndarray): The 1D array of pixels.
        height (int): The height of the original image.
        width (int): The width of the original image.

    Yields:
        np.ndarray: An 8x8 numpy array (block) of pixels.
    """
    if len(pixels_1d) != height*width:
        raise ValueError("1D byte array does match specified height/width. Check your slicing.")

    # reshape the 1D array into a 2D array
    pixels_2d = np.array(pixels_1d).reshape((height, width))

    # iterate over the 2D array in 8x8 blocks
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            block = pixels_2d[y:y+8, x:x+8]

            if block.shape == (8, 8):
                # There's an opportunity to pad a non-square block here
                yield block

def main(png_name, filt, thresh):
    if png_name.split('.')[-1] != 'png':
        print(f"Uh oh. {png_name} is not a .png file, I can't Doodle this.")
        return

    img = Image.open(png_name)
    # img.convert('L') converting to greyscale might work for SOME pngs. But for those that are just all black with varying levels of alpha, it will not work. Parameter?
    img_width, img_height = img.size
    print(f"Original image size {img_width} x {img_height}")
    
    # resize image to be multiple of 8 wide/tall 
    print(f"Cropping image by {img_width % 8} x {img_height % 8}")
    img_width = img_width - (img_width % 8)
    img_height = img_height - (img_height % 8)
    img = img.crop((0,0,img_width, img_height))

    sample_pixel = img.getpixel((0,0))
    byte_stream = img.tobytes()

    pix = []
    pixel_size = i2 = len(sample_pixel)
    i  = 0
    for j in range(int(len(byte_stream)/pixel_size)):
        pix.append(byte_stream[i:i2])
        i   = i2
        i2 += pixel_size

    def pad_string(s):
        if len(s) % 2 != 0:
            return '0' + s
        return s

    b = b''
    #pix = [p[-1] for p in pix] if pixel_size > 1 else [p[0] for p in pix] 
    if filt == "red":
        pix = [255 if (p[0]) < thresh else 0 for p in pix]
    elif filt == "blue":
        pix = [255 if (p[1]) < thresh else 0 for p in pix]
    elif filt == "green":
        pix = [255 if (p[2]) < thresh else 0 for p in pix]
    elif filt == "alpha":
        pix = [255 if (p[3]) < thresh else 0 for p in pix]
    elif filt == "mean":
        pix = [255 if (p[0] + p[1] + p[2])/3 < thresh else 0 for p in pix]
    # Iterate and process each block
    for i, block in enumerate(iterate_8x8_blocks(pix, img_height, img_width)):
        print(f"Block {i+1}:")
        print(block)
        for line in block:
            for p in line:
                if p == 255: #binascii.unhexlify(pad_hex_string(hex(p)[2:])) != b'\x00': #b'\xff':
                    b += b'1'
                else:
                    b += b'0'
    b_final = [b[i:i+8] for i in range(0, len(b), 8)]

    outfile = png_name.split('.')[0] + pad_string(hex(img_width // 8).split('x')[-1]) + 'x' + pad_string(hex(img_height // 8).split('x')[-1]) + '.icn'
    with open(outfile, "ab") as f:
        for byte in b_final:
            f.write(int(byte,2).to_bytes(1, byteorder='big'))
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--png_in", required=True, help=".png filename to be convreted to .icn")
    parser.add_argument('-f', "--filter", choices=("red", "blue", "green", "alpha", "mean"), default="mean", help="Filter target, what to use to convert pixel to black or white ('red', 'blue', 'green', 'alpha', 'mean').")
    parser.add_argument('-t', "--threshold", type=int, default=150, help="Filter threshold 0 to 255. Values < are black pixels, otherwise white.")
    args = parser.parse_args()
    png_name = args.png_in
    filt = args.filter
    thresh = args.threshold
    # png_name = "50-iceland-farm.png"
    # filt= "mean"
    # thresh = 150
    main(png_name, filt, thresh)
