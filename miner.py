import apt
from operator import itemgetter

from collections import OrderedDict


c = apt.Cache()
keys = c.keys()

MIN_LETTERS = 6


l = {}
count = 0
for k in keys:
    count += 1
    n = c[k].name
    print("scanning",count, n)

    wl = len(n)

    idx = 0

    if wl < MIN_LETTERS:
        min_length = wl
    else:
        min_length = MIN_LETTERS

    while idx < wl - min_length:
        tail_idx = idx + min_length

        while tail_idx < wl:
            part = n[idx:tail_idx]

            try:
                l[part] += 1

            except:
                l[part] = 1

            tail_idx += 1

        idx += 1


slist = OrderedDict(sorted(l.items(), key = itemgetter(1), reverse = True))


i = 0

for k in slist.keys():
    print(k, slist[k])

    if i == 100:
        break
    else:
        i+=1


