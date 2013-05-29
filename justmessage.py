#!/usr/bin/env python3
from tkinter import *

def main(message, font='Monospace 30', title='just a message'):
    root = Tk()
    root.wm_title(title)
    label = Label(root, text=message, font=font).pack()
    root.mainloop()

def set_terminal_caption():
    import sys
    sys.stdout.write('\033]2;' + sys.argv[0].rpartition('/')[2] + '\007')
    sys.stdout.flush()

if __name__ == '__main__':
    set_terminal_caption()

    import argparse
    parser = argparse.ArgumentParser(prog='justmessage', description="just display a message")
    parser.add_argument('message')
    parser.add_argument('-f', '--font')
    parser.add_argument('-t', '--title')
    args = parser.parse_args()

    kwargs = {}
    if args.font is not None:
        kwargs.update(font=args.font)
    if args.title is not None:
        kwargs.update(title=args.title)
    main(args.message, **kwargs)

