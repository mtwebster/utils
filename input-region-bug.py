import sys
import cairo
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(500, 500)

        label = Gtk.Label(label="指针穿透窗体")
        self.add(label)
        self.set_keep_above(True)
        self.set_app_paintable(True)
        # self.set_decorated(False)
        screen: Gdk.Screen = self.get_screen()
        visual = screen.get_rgba_visual()
        self.set_visual(visual)

    def do_map_event(self, *args):
        orig_x = self.get_allocated_width()
        orig_y = self.get_allocated_height()

        rect = cairo.RectangleInt(x=orig_x, y=orig_y, width=self.get_allocated_width(),
                                  height=self.get_allocated_height())
        region = cairo.Region(rect)
        self.input_shape_combine_region(region)
        # self.shape_combine_region(region)


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self,
                                    title="指针穿透窗体", type=Gtk.WindowType.TOPLEVEL)
        self.window.show_all()
        self.window.present()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)