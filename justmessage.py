#!/usr/bin/env python3
from tkinter import *

PROG = 'justmessage'

def main(*, message, font, font_size, title):
    root = Tk()
    root.wm_title(title)
    label = Label(root, text=message, font='{} {}'.format(font, font_size))
    label.pack()
    root.mainloop()

def set_terminal_caption(caption=None):
    import sys
    if caption is None:
        caption = sys.argv[0].rpartition('/')[2]
    sys.stdout.write('\033]2;' + caption + '\007')
    sys.stdout.flush()

if __name__ == '__main__':
    set_terminal_caption(PROG)

    import argparse
    parser = argparse.ArgumentParser(prog=PROG,
        description='just display a message' )
    parser.add_argument('message')
    parser.add_argument('-F', '--font', default='Sans')
    parser.add_argument('-f', '--font-size', type=int,
        default=100,
        help='label font size' )
    parser.add_argument('-t', '--title', default='just a message')
    args = parser.parse_args()

    main(**vars(args))

