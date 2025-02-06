from PIL import Image
from PIL import ImageOps
import argparse
import time

def main(icn_name):
    tock = time.time()
    print(f"Let's Poodle this Noodle: {icn_name}")
    with open(icn_name, 'rb') as f:
        images = [ImageOps.invert(Image.frombytes(mode='1', size=[8,8], data=chunk)) for chunk in iter(lambda: f.read(8), b'')]

    # gather and concatenate images in rows of 72
    print("Building rows...")
    rows = []
    for n in range(1,47):
        x_offset=0
        row = images[72*(n-1):72*n]
        row_im = Image.new('1', (len(row)*8, 8))
        for im in row:
            row_im.paste(im, (x_offset,0))
            x_offset += im.size[0]
        rows.append(row_im)

    print("Stacking rows...")
    y_offset = 0
    final_im = Image.new('1', (rows[0].size[0], len(rows)*8))
    for row in rows:
        final_im.paste(row, (0,y_offset))
        y_offset += 8

    out_name = icn_name.split('.')[0] + '.png'
    final_im.save(out_name)
    tick = time.time()
    print(f"{out_name}")
    print(f"Poodled in {tick-tock:.3f} s.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--icn_in")
    args = parser.parse_args()
    icn_name = args.icn_in
    main(icn_name)
# noodles are 568 x 368; 26128 bytes