import gi
gi.require_version('Gdk', '2.0')
from gi.repository import Gdk

screen = Gdk.Screen.get_default ();
mdm_wm_num_monitors = screen.get_n_monitors();

print("Number of monitors found: %d" % mdm_wm_num_monitors)

if (mdm_wm_num_monitors > 1):
    for i in range(0,mdm_wm_num_monitors):
        plugname = screen.get_monitor_plug_name (i);
        print plugname
