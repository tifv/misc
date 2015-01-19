def main(*, seconds, precision, flavour, ui, immediate, font_size):
    if flavour == 'regular':
        from .core import TimerCore as FlavourTimerCore
        title = 'Regular timer'
    elif flavour == 'poisson':
        from .flavour.poisson import PoissonTimerCore as FlavourTimerCore
        title = 'Poisson timer'
    elif flavour == 'wiener':
        from .flavour.wiener import WienerTimerCore as FlavourTimerCore
        title = 'Wiener timer'
    else:
        raise ValueError(flavour)
    if ui == 'gtk':
        from .ui.gtk import GtkTimerCore as UITimerCore
    elif ui == 'qt':
        from .ui.qt import QtTimerCore as UITimerCore
    elif ui == 'tk':
        from .ui.tk import TkTimerCore as UITimerCore
    else:
        raise ValueError(ui)
    class TheTimerCore(UITimerCore, FlavourTimerCore):
        pass
    core = TheTimerCore(seconds, precision, title=title, font_size=font_size)
    if immediate:
        core.start()
    core.mainloop()

def set_terminal_caption(caption=None):
    import sys
    if caption is None:
        caption = sys.argv[0].rpartition('/')[2]
    sys.stdout.write('\033]2;' + caption + '\007')
    sys.stdout.flush()

