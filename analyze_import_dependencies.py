#!/usr/bin/env python


"""
Author: RockLee <insfocus@gmail.com>
Website: code-trick.com
Version: 0.1-alpha

Get the detailed import dependencies of your python script,
mostly used to analyze unused importing.

"""

import sys
import traceback
import getopt


class Importer(object):
    def __init__(self):
        self.cached = {}

    def find_module(self, fullname, path):
        stack = traceback.extract_stack()
        last_key = None
        for filename, lineno, func, stmt in stack[:-1]:
            self.cached.setdefault(last_key, {})
            key = (filename, lineno)
            self.cached[last_key][key] = stmt
            last_key = key

        return None


def cmp(a, b):
    if a[1] < b[1]:
        return -1
    elif a[1] == b[1]:
        return 0
    else:
        return 1


def skip_module(k, patterns=[]):
    for pattern in patterns:
        if k.find(pattern) >= 0:
            return True

    return False


def output(level=0, key=None, max=10, ignore_patterns=[]):
    if level >= max:
        return

    if key and skip_module(key[0], ignore_patterns):
        return

    keys = importer.cached.get(key, {}).keys()
    keys.sort(cmp=cmp)

    for k in keys:
        v = importer.cached.get(key, {}).get(k)
        if skip_module(k[0], ignore_patterns):
            print '  '*level, '<----- omitted ----->'
            continue
        print '  '*level, k[0], ':', k[1], '(', v, ')'
        if importer.cached.get(k):
            output(level+1, k, ignore_patterns=ignore_patterns)


def usage():
    print 'python dump_import_dep.py -s stmt -l level(default to 10) [--ignore-pattern=xx]'


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:d:", ["stmt=", "level=", "ignore-pattern="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(1)

    stmt = None
    level = 10
    ignore_patterns = []
    for o, a in opts:
        if o in ('-s', '--stmt'):
            stmt = a

        elif o in ('-l', '--level'):
            level = int(a)

        elif o in ('--ignore-pattern'):
            ignore_patterns.append(a)

    if stmt is None or level < 0:
        usage()
        sys.exit(1)

    importer = Importer()
    sys.meta_path = [importer]

    exec(stmt)

    output(ignore_patterns=ignore_patterns)
