#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from dorgen import dorgen
from dorgen.exceptions import Error

def usage():
    s = """
    Usage: %s <textfile> <kwfile> <template> [folder]

    This script provides generation of texts by keywords
        <textfile> - file with template text
        <kwfile> - file with keywords
        <template> - Folder with .thtml files
        [folder] - deploy folder
    """ % sys.argv[0]
    print s


argv = sys.argv[1:]

if len(argv) < 2:
    usage()
    exit(2)

try:
    dorgen = dorgen.Dorgen(*argv[:4])
    dorgen.run()
    print "[OK] Script executed successfully"
except Error as e:
    print "[FAIL] Error while executing the script"
    print e