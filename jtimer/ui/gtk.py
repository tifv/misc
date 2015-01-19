from gi.repository import Gtk, GObject

from ..core import TimerCore

class GtkTimerCore(TimerCore):
    def __init__(self, *args, title, font_size, **kwargs):
        def close_handler(widget, event):
            self.close()
        def clicked_handler(widget):
            self.interact()

        self.master = Gtk.Window(title=title)
        self.label = Gtk.Label()
        self.master.connect('delete-event', close_handler)
        self.master.add(self.label)
        self.label_font_size = int(1000 * font_size)

        self.control = Gtk.Window(
            title=title + ' (control)',
            default_width=150, default_height=150
        )
        self.control.connect('delete-event', close_handler)
        self.button = Gtk.Button()
        self.button.set_label('Start/Pause')
        self.button.connect('clicked', clicked_handler)
        self.control.add(self.button)

        self.timeout_id = None

        self.master.show_all()
        self.control.show_all()

        super().__init__(*args, **kwargs)

    def start_timeout(self):
        assert self.timeout_id is None
        def timeout_call():
            self.update()
            return True # continue timeout
        self.timeout_id = GObject.timeout_add(25, timeout_call)

    def stop_timeout(self):
        assert self.timeout_id is not None
        GObject.source_remove(self.timeout_id)
        self.timeout_id = None

    def mainloop(self):
        return Gtk.main()

    def shutdown(self):
        Gtk.main_quit()

    def set_label_text(self, text, finished=False):
        self.label.set_markup(
            '<span font_size="{size}" foreground="{colour}">{text}</span>'
            .format(text=text,
                colour='black' if not finished else 'red',
                size=self.label_font_size )
        )

