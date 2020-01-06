#!/usr/bin/python3

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gtk
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class Main:
    def __init__(self):
        self.screen = Gdk.Screen.get_default();
        self.display = Gdk.Display.get_default()

        self.report_screen()
        self.report_display()

        self.display.connect("monitor-added", self.on_display_monitor_added_or_removed)
        self.display.connect("monitor-removed", self.on_display_monitor_added_or_removed)

        self.screen.connect("size-changed", self.on_screen_size_changed)
        self.screen.connect("monitors-changed", self.on_screen_size_changed)

    def on_display_monitor_added_or_removed(self, display, monitor, data=None):
        print("Monitor added or removed")
        self.report_display()

    def on_screen_size_changed(self, screen, data=None):
        print("Screen changed")
        self.report_screen()

    def report_screen(self):
        n_monitors = self.screen.get_n_monitors()
        w = self.screen.get_width()
        h = self.screen.get_height()

        print("Screen: n_monitors: %d, size: %d, %d" % (n_monitors, w, h))

    def report_display(self):
        n_monitors = self.screen.get_n_monitors()
        print("Display: n_monitors: %d" % (n_monitors))

if __name__ == "__main__":

    main = Main()

    Gtk.main()


