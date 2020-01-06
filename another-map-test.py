#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

import time, threading

# Used as a decorator to time functions
def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print('%s took %0.3f ms' % (func.__name__, (t2 - t1) * 1000.0))
        return res
    return wrapper

# Used as a decorator to run things in the background
def async(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper

# Used as a decorator to run things in the main loop, from another thread
def idle(func):
    def wrapper(*args):
        GObject.idle_add(func, *args)
    return wrapper

class MyApp ():

    def __init__(self):
        self.windows = []
        mainwindow = Gtk.Window()
        box = Gtk.Box()
        button = Gtk.Button()
        button.set_label("Open windows")
        button.connect("clicked", self.make_windows)
        box.pack_start(button, False, False, 0)
        button = Gtk.Button()
        button.set_label("Close windows")
        button.connect("clicked", self.close_windows)
        box.pack_start(button, False, False, 0)
        mainwindow.add(box)
        mainwindow.show_all()
        mainwindow.connect("destroy", Gtk.main_quit)

    @print_timing
    def make_windows(self, widget):
        for i in range(200):
            window = Gtk.Window()
            self.windows.append(window)
            window.show()

    @print_timing
    def close_windows(self, widget):
        for window in self.windows:
            window.destroy()
        self.windows = []


MyApp()
Gtk.main()

