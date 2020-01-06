#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GObject
class Main:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('frameclock-test.glade')

        self.window = self.builder.get_object('window')
        self.window.connect("delete-event", self.end)

        self.spinner = self.builder.get_object('spinner')

        self.toggle = self.builder.get_object('toggle')
        self.toggle.bind_property('active', self.spinner, 'active', GObject.BindingFlags.DEFAULT)

        self.button = self.builder.get_object('misc')
        self.button.connect("clicked", self.on_button_clicked)

        self.window.show_all()

    def on_button_clicked(self, widget, data=None):
        w = self.window.get_window()

        w.lower()

    def end(self, event, data=None):
        Gtk.main_quit()

if __name__ == "__main__":
    Main()
    Gtk.main()
