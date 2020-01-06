// build by gcc -o test2 -g -O0 test2.c `pkg-config --libs --cflags gtk+-3.0`

#include <gtk/gtk.h>
#include <gdk/gdk.h>

GtkWidget *window;
GtkWidget *shell;
GtkWidget *drawing;
GdkWindow *gdkwindow;

gint test_callback(gpointer data)
{
  static int state = 0;

  struct GdkEventConfigure {
    GdkEventType type;
    GdkWindow *window;
    gint8 send_event;
    gint x, y;
    gint width;
    gint height;
  } event = { GDK_CONFIGURE, gtk_widget_get_window(GTK_WIDGET(shell)), 
              TRUE, 0, 0, 50, 50};

  switch(state) {
    case 0:
      // Original position
      gtk_window_move(GTK_WINDOW(shell), 0, 0);
      gtk_window_resize(GTK_WINDOW(shell), 50, 50);
      gtk_widget_show(GTK_WIDGET(shell));
      break;
    case 1:
      gtk_widget_hide(GTK_WIDGET(shell));
      // Send configure event when widget is hidden
      // with correct position (0,0) (50,50)
      gtk_main_do_event(&event);
      break;
    case 2:
      gtk_window_move(GTK_WINDOW(shell), 0, 500);
      break;
    case 3:
      // shell widget has priv->configure_notify_received = TRUE
      // so it resets to last saved configure event (0,0) instead of the new one (0,500)
      // gtk_window_move_resize() gtkwindow.c:9339
      gtk_widget_show(GTK_WIDGET(shell));
      break;
    case 4:
      gtk_widget_hide(GTK_WIDGET(shell));
      // Send configure event when widget is hidden
      // with correct position (0,500) (50,50)
      event.x = 0;
      event.y = 500;
      gtk_main_do_event(&event);
      break;
    case 5:
      // wrong position -> 0,0
      gtk_widget_show(GTK_WIDGET(shell));
      break;
    default:
      return FALSE;
  }

  state++;
  return TRUE;
}

static void draw_tooltip_cb(GtkWidget *widget, cairo_t* cr,
                            gpointer   data )
{
    cairo_rectangle (cr, 0, 0, 100, 100);
    cairo_set_source_rgb (cr, 1, 0, 0);
    cairo_fill (cr);
}

/* Another callback */
static void destroy( GtkWidget *widget,
                     gpointer   data )
{
    gtk_main_quit ();
}

int main( int   argc,
          char *argv[] )
{
    gtk_init (&argc, &argv);

    /* create a new window */
    window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
    drawing = gtk_drawing_area_new();
    gtk_container_add(GTK_CONTAINER(window), drawing);

    g_signal_connect (window, "destroy",
          G_CALLBACK (destroy), NULL);

    gtk_widget_show_all (GTK_WIDGET(window));

    shell = gtk_window_new(GTK_WINDOW_POPUP);
    gtk_window_set_type_hint (GTK_WINDOW(shell), GDK_WINDOW_TYPE_HINT_TOOLTIP);
    gtk_window_set_transient_for(GTK_WINDOW(shell), GTK_WINDOW(window));
    g_signal_connect (shell, "draw",
          G_CALLBACK (draw_tooltip_cb), NULL);
    gtk_widget_set_app_paintable (shell, TRUE);

    g_timeout_add (500, test_callback, 0);

    gtk_main ();

    return 0;
}
