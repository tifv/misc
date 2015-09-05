#!/usr/bin/python3

import collections
import random

import sys

import argparse

import yaml

ITALIC = '\033[3m'
UPRIGHT = '\033[23m'

def repeat(sequence):

    queue = collections.deque()

    pool = collections.deque(random.sample(sequence, len(sequence)))
    def pool_pop():
        return pool.pop()
    def pool_add(element, _methods=(pool.append, pool.appendleft)):
        random.choice(_methods)(element)

    while True:
        while len(queue) < len(pool):
            queue.appendleft(pool_pop())
        e = queue.pop()
        yield e
        pool_add(e)

def mainloop(data, key):
    if not any(key in item for item in data):
        raise ValueError("Key not present in cards: {}".format(key))
    for item in repeat(data):
        item = item.copy()
        try:
            print(key + ': ' + ITALIC + item.pop(key) + UPRIGHT, end='')
        except KeyError:
            continue
        sys.stdout.flush()
        s = sys.stdin.readline()
        if not s:
            raise EOFError
        print(yaml.dump( item,
            allow_unicode=True, default_flow_style=False ))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('key')
    parser.add_argument(metavar='datafile', dest='filenames', nargs='+')

    args = parser.parse_args()

    data = []
    for filename in args.filenames:
        with open(filename, 'r') as datafile:
            data_piece = yaml.load(datafile)
            assert isinstance(data_piece, list)
            data.extend(data_piece)
    try:
        mainloop(data, args.key)
    except (KeyboardInterrupt, EOFError):
        print() # clear the line
        return

if __name__ == '__main__':
    main()

