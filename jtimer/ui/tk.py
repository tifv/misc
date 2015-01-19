from tkinter import Tk, Toplevel, Label, Button

from ..core import TimerCore

class TkTimerCore(TimerCore):
    def __init__(self, *args, title, font_size, **kwargs):
        def close_handler(event):
            self.close()
        def clicked_handler(event):
            self.interact()

        self.master = Tk()
        self.master.wm_title(title)
        self.master.bind('<Destroy>', close_handler)
        self.label = Label(self.master, font='Sans {}'.format(int(font_size)))
        self.label.pack(expand=True)

        self.control = Toplevel()
        self.control.wm_title(title + ' (control)')
        self.control.minsize(150, 150)
        self.control.bind('<Destroy>', close_handler)
        self.button = Button(self.control, text='Start/Pause')
        self.button.bind('<ButtonRelease>', clicked_handler)
        self.button.pack(expand=True)

        self.timeout_running = False

        super().__init__(*args, **kwargs)

    def start_timeout(self):
        assert self.timeout_running is False
        def timeout_call():
            if self.timeout_running:
                self.update()
                self.master.after(25, timeout_call)
        self.timeout_running = True
        timeout_call()

    def stop_timeout(self):
        assert self.timeout_running is True
        self.timeout_running = False

    def mainloop(self):
        return self.master.mainloop()

    def shutdown(self):
        self.master.quit()

    def set_label_text(self, text, finished=False):
        self.label.config(text=text)
        if finished:
            self.label.config(fg='red')

