#!/usr/bin/env python
# -*- set coding: utf-8 -*-

import os
import sys
from parerga import db


usage = '''usage:
    {} add <entry>...
    {} initdb
'''.format(__file__, __file__)

def add_entries(entries):
    ids = []
    for entry_path in entries:
        idx = db.add_entry(entry_path)
        print("Added entry at '%s'" % entry_path)
        ids.append(idx)
    return ids

def init_db():
    return db.init_db()

def try_add(entries):
    result = add_entries(entries)
    if result:
        print(result)
    else:
        print(usage)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) > 0:
        if args[0] == 'add':
            try_add(args[1:])
        elif args[0] == 'initdb':
            init_db()
        else:
            print(usage)
    else:
        print(usage)
