from . import main, set_terminal_caption

if __name__ == '__main__':
    set_terminal_caption()

    import argparse
    parser = argparse.ArgumentParser(
        prog='mytimer', description="Timer" )
    parser.add_argument('minutes', type=float,
        metavar='DURATION', help='duration in minutes' )
    parser.add_argument('-p', '--precision', type=int,
        default=0, const=1, nargs='?',
        help='print fractions of seconds' )
    parser.add_argument('-i', '--immediate',
        action='store_true',
        help='Start timer immediately')

    flavour_group = parser.add_mutually_exclusive_group()
    flavour_group.add_argument('-P', '--poisson',
        action='store_const', dest='flavour', const='poisson',
        help='Poisson timer' )
    flavour_group.add_argument('-W', '--wiener',
        action='store_const', dest='flavour', const='wiener',
        help='Wiener timer' )
    parser.set_defaults(flavour='regular')

    ui_group = parser.add_mutually_exclusive_group()
    ui_group.add_argument('--tk',
        action='store_const', dest='ui', const='tk')
    parser.set_defaults(ui='gtk')

    args = parser.parse_args()
    if (args.precision < 0):
        parser.error('precision must be non-negative')

    main(**vars(args))

