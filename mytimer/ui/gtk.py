from gi.repository import Gtk, GObject

from .common import CommonTimerApp

class GtkTimerApp(CommonTimerApp):
    def __init__(self, timer, precision, title='timer'):
        super().__init__(timer, precision)

        self.master = Gtk.Window(title=title)
        self.master.connect('delete-event', Gtk.main_quit)
        self.master.connect('key-release-event', self.key_release)

        self.label = Gtk.Label()
        self.master.add(self.label)
        self.show_remained(None)

        self.on_space_key = self.start_timer
        self.master.show_all()

    def key_release(self, widget, event):
        if event.keyval == 32:
            self.on_space_key()

    def start_timer(self):
        super().start_timer()
        GObject.timeout_add(20, self.show_remained, None)
        self.show_remained(None)
        self.on_space_key = self.break_timer

    def break_timer(self):
        super().break_timer()
        Gtk.main_quit()

    def quit_timer(self):
        Gtk.main_quit()

    def mainloop(self):
        return Gtk.main()

    def show_remained(self, userdata=None):
        assert userdata is None
        remained = self.timer.remained()
        if remained <= 0:
            self.finish_timer()
            return False # end timeout
        self.set_markup(self.format_remained(remained))
        return True

    def finish_timer(self):
        self.set_markup(self.format_remained(0.0), fg='red')
        self.on_space_key = self.quit_timer

    def set_markup(self, s, fg='black'):
        self.label.set_markup(
            '<span font_size="100000" foreground="{fg}">{0}</span>'
            .format(s, fg=fg) )

