from . import core

def main(minutes, precision=0, flavour='regular', ui='tk', immediate=False):
    seconds = minutes * 60
    if flavour == 'regular':
        Timer = core.RegularTimer
    elif flavour == 'poisson':
        Timer = core.PoissonTimer
    elif flavour == 'wiener':
        Timer = core.WienerTimer
    else:
        raise ValueError(flavour)
    if ui == 'tk':
        from .ui.tk import TkTimerApp as TimerApp
    elif ui == 'gtk':
        from .ui.gtk import GtkTimerApp as TimerApp
    else:
        raise ValueError(ui)
    app = TimerApp(Timer(seconds), precision)
    if immediate:
        app.start_timer(event=None)
    app.mainloop()

def set_terminal_caption():
    import sys
    sys.stdout.write('\033]2;' + sys.argv[0].rpartition('/')[2] + '\007')
    sys.stdout.flush()

