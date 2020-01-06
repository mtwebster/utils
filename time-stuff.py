#!/usr/bin/python3

from gi.repository import GLib

import time


tz = GLib.TimeZone.new_local()


iterations = 100000

#############################################
start = time.perf_counter()

for x in range(0, iterations):
    j = GLib.DateTime.new_now_local()

end = time.perf_counter()
elapsed = end - start

print("GLib.DateTime.new_now_local(): %f seconds" % elapsed)
################################################

start = time.perf_counter()

for x in range(0, iterations):
    j = GLib.DateTime.new_now(tz)

end = time.perf_counter()
elapsed = end - start

print("GLib.DateTime.new_now(tz): %f seconds" % elapsed)
###############################################
start = time.perf_counter()

for x in range(0, iterations):
    j = GLib.DateTime.new_from_unix_local(100000000)

end = time.perf_counter()
elapsed = end - start

print("GLib.DateTime.new_from_unix_local(t): %f seconds" % elapsed)
###############################################
start = time.perf_counter()

for x in range(0, iterations):
    j = GLib.DateTime.new_from_unix_utc(100000000).to_timezone(tz)

end = time.perf_counter()
elapsed = end - start

print("GLib.DateTime.new_from_unix_utc(t).to_timezone(tz): %f seconds" % elapsed)
