import argparse
from PIL import Image, ImageOps
import os
import hashlib
import sys
import re
from .util import *


def main():
    parser = argparse.ArgumentParser(description="Create an image from a md5 hash")
    parser.add_argument("input", help="Input string to hash")
    parser.add_argument("-d", action="store_true", help="debug mode")
    parser.add_argument("-i", action="store_true", help="invert the image")
    parser.add_argument("--md5", action="store_true", help="give an md5 hash directly")
    parser.add_argument("-c", action="store_true", help="console mode")
    args = parser.parse_args()

    hash = hashlib.md5(args.input.encode()).hexdigest() if not args.md5 else args.input.lower()

    pattern = re.compile(r'^[a-f0-9]{32}$')
    match = pattern.match(hash)
    if not match:
        sys.stderr.write(f'{hash} is not a valid MD5 hash\n')
        sys.exit(-1)

    if args.d:
        sys.stdout.write(
            f'hashpic: "{args.input}" will be following hash: {hash}\n'
            if not args.md5
            else f"hashpic: directly given hash: {args.input}\n"
        )

    if args.c:
        chunks = chunk_it(chunk_it(hash), 4)

        for i in chunks:
            for j in i:
                sys.stdout.write(
                    f"\033[38;5;{0xff - int(j, 16) if args.i else int(j, 16)}m{j}\u001b[0m"
                )
            sys.stdout.write("\n")
        sys.exit(0x00)

    colors = []
    for i in chunk_it(hash):
        colors.append(convert_term_to_rgb(int(i, 16)))

    width = 1024
    height = 1024

    im = Image.new(mode="RGB", size=(width, height), color="#ffffff")
    pixels = im.load()
    for x in range(width):
        for y in range(height):
            if x < 0x100 and y < 0x100:
                pixels[x, y] = colors[0]
            elif x < 0x200 and y < 0x100:
                pixels[x, y] = colors[1]
            elif x < 0x300 and y < 0x100:
                pixels[x, y] = colors[2]
            elif x < 0x400 and y < 0x100:
                pixels[x, y] = colors[3]
            elif x < 0x100 and y < 0x200:
                pixels[x, y] = colors[4]
            elif x < 0x200 and y < 0x200:
                pixels[x, y] = colors[5]
            elif x < 0x300 and y < 0x200:
                pixels[x, y] = colors[6]
            elif x < 0x400 and y < 0x200:
                pixels[x, y] = colors[7]
            elif x < 0x100 and y < 0x300:
                pixels[x, y] = colors[8]
            elif x < 0x200 and y < 0x300:
                pixels[x, y] = colors[9]
            elif x < 0x300 and y < 0x300:
                pixels[x, y] = colors[10]
            elif x < 0x400 and y < 0x300:
                pixels[x, y] = colors[11]
            elif x < 0x100 and y < 0x400:
                pixels[x, y] = colors[12]
            elif x < 0x200 and y < 0x400:
                pixels[x, y] = colors[13]
            elif x < 0x300 and y < 0x400:
                pixels[x, y] = colors[14]
            elif x < 0x400 and y < 0x400:
                pixels[x, y] = colors[15]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)

    if args.i:
        im = ImageOps.invert(im)

    if args.d:
        im.show()

    im.save(os.getcwd() + "/output.png")


if __name__ == "__main__":
    main()