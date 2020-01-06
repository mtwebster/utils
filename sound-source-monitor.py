#!/usr/bin/env python3

import gi
gi.require_version('Cvc', '1.0')

from gi.repository import Cvc, GLib

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class Main:
    def __init__(self):
        self.controller = Cvc.MixerControl(name = "sound-source-monitor")

        self.controller.connect("stream-added", self.stream_added)
        self.controller.connect("stream-removed", self.stream_removed)

    def stream_added(self, controller, sid):
        s = controller.lookup_stream_id(sid)
        if s == None:
            return


        print("Stream added:", s.get_application_id(),
                               s.get_name(),
                               s.get_description(),
                               s.get_sysfs_path())


    def stream_removed(self, controller, sid):
        s = controller.lookup_stream_id(sid)
        if s == None:
            return

        print("Stream removed:", s.get_application_id(),
                                 s.get_name(),
                                 s.get_description(),
                                 s.get_sysfs_path())

if __name__ == "__main__":

    main = Main()

    GLib.MainLoop.new(None, True).run()