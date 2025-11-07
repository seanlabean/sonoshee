from PIL import Image
from PIL import ImageOps
import argparse

def main(icn_name):
    if icn_name.split('.')[-1] != 'icn':
        print(f"Uh oh. {icn_name} is not a .icn file, I can't Poodle this.")
        return
    try:
        print(f"{icn_name} :: Let's Poodle this Noodle")
        with open(icn_name, 'rb') as f:
            images = [ImageOps.invert(Image.frombytes(mode='1', size=[8,8], data=chunk)) for chunk in iter(lambda: f.read(8), b'')]

        # get num rows/cols from hex encoded filename
        width = int(icn_name[-9:-7], 16)
        height = int(icn_name[-6:-4], 16)

        # gather and concatenate images into width rows of height
        print("~ Building rows...")
        rows = []
        for n in range(1,height+1):
            x_shift=0
            row = images[width*(n-1):width*n]
            row_im = Image.new('1', (len(row)*8, 8))
            for im in row:
                row_im.paste(im, (x_shift,0))
                x_shift += im.size[0]
            rows.append(row_im)

        print("~ Stacking rows...")
        y_shift = 0
        final_im = Image.new('1', (rows[0].size[0], len(rows)*8))
        for row in rows:
            final_im.paste(row, (0,y_shift))
            y_shift += row.size[1]

        out_name = icn_name.split('.')[0] + '.png'
        final_im.save(out_name)
        print(f"{out_name}")
        return
    except Exception as e:
        print(f"Uh oh. I tried to Poodle {icn_name} but failed.")
        print(f"Are you sure this is a Noodle to Poodle?")
        print(e)
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--icn_in")
    args = parser.parse_args()
    icn_name = args.icn_in
    main(icn_name)
# dimensions of .icn image data are encoded in the file names themselves as hex
# noodles are 568 x 368; 26128 bytes