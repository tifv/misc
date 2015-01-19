from . import main, set_terminal_caption

PROG = 'jtimer'

if __name__ == '__main__':
    set_terminal_caption(PROG)

    import argparse
    parser = argparse.ArgumentParser(
        prog=PROG, description='Timer' )
    parser.add_argument('seconds', type=float,
        metavar='DURATION', help='timer duration' )
    parser.add_argument('-p', '--precision', type=int,
        default=0, const=1, nargs='?',
        help='print fractions of seconds' )
    parser.add_argument('-i', '--immediate',
        action='store_true',
        help='start timer immediately' )
    parser.add_argument('-f', '--font-size', type=float,
        default=100,
        help='label font size' )

    flavour_group = parser.add_mutually_exclusive_group()
    flavour_group.add_argument('-P', '--poisson',
        action='store_const', dest='flavour', const='poisson',
        help='launch Poisson timer' )
    flavour_group.add_argument('-W', '--wiener',
        action='store_const', dest='flavour', const='wiener',
        help='launch Wiener timer' )
    parser.set_defaults(flavour='regular')

    ui_group = parser.add_mutually_exclusive_group()
    ui_group.add_argument('--gtk',
        action='store_const', dest='ui', const='gtk',
        help='use GTK+ 3' )
    ui_group.add_argument('--qt',
        action='store_const', dest='ui', const='qt',
        help='use Qt 4 (default)' )
    ui_group.add_argument('--tk',
        action='store_const', dest='ui', const='tk',
        help='use Qt 4 (default)' )
    parser.set_defaults(ui='tk')

    args = parser.parse_args()
    if args.precision < 0:
        parser.error('precision must be non-negative')
    if args.precision > 0 and args.flavour == 'poisson':
        parser.error('Poisson timer does not allow non-zero precision')

    main(**vars(args))

